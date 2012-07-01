; number of cars
(def car_count (ref 2))

; number of SUV
(def suv_count (ref 2))

;increment car count if the total sum of car and suv is less than 5
(def increment_car (Thread. (fn []
                              (dosync
                                ;if sum of (cars + suv) <= 5 then increment car
                                (if (< (+ (deref car_count) (deref suv_count)) 5) ;
                                  (alter car_count inc))))))

;increment suv count if the total sum of car and suv is less than 5
(def increment_suv (Thread. (fn []
                              (dosync
                                ;if sum of (cars + suv) <= 5 then increment suv
                                (if (< (+ (deref car_count) (deref suv_count)) 5) ;
                                  (alter suv_count inc))))))

(doseq [p [increment_car increment_suv]] (.start p))
(doseq [p [increment_car increment_suv]] (.join p))

(if (> (+ (deref car_count) (deref suv_count)) 5)
  (println "write skew detected"))
(if (<= (+ (deref car_count) (deref suv_count)) 5)
  (println "no write skew detected")) ;