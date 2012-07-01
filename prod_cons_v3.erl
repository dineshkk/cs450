-module(prod_cons_v3).
-export([start/0]).
-define(MAX_VAL, 20).
-define(MAX_AHEAD, 3).

consume_ack(0,0) -> 0;
consume_ack(0,Ahead) -> Ahead;
consume_ack(Attempt,Ahead) ->
	%io:format("consume_ack: Attempt:~w Ahead by ~w~n", [Attempt,Ahead]),
	receive
		ack -> 
			io:format("P: got confirmation on retry, ahead by ~w~n", [Ahead - 1]),
			consume_ack(Attempt,Ahead - 1)
		after
			3 ->
			consume_ack(Attempt-1,Ahead)
	end.
            
producer(Val, Consumer, Ahead) ->
    if Val =:= ?MAX_VAL ->	
            Consumer ! terminate;
       Ahead =:= ?MAX_AHEAD ->
            io:format("P: throttling!~n"),
            receive
                ack -> producer(Val, Consumer, Ahead - 1)
            end;
       true ->
		   	timer:sleep(random:uniform(500)),  % producing!
            Consumer ! {self(), Val},            
			receive
                ack -> io:format("P: got confirmation, ahead by ~w~n", [Ahead]),
				producer(Val + 1, Consumer, Ahead)
            after
				0 -> 
				T = consume_ack(10,Ahead + 1),
    			producer(Val + 1, Consumer, T)
        end
    end.

consumer() ->
    receive
        terminate -> done;
        {Producer, Val} -> io:format("C: got ~w~n", [Val]),
                           timer:sleep(random:uniform(400)),  % consuming
                           Producer ! ack,
                           consumer()
    end.

start() ->
    C = spawn(fun consumer/0),
    spawn(fun() -> producer(0, C, 0) end).
