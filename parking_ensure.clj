; number of cars
(def car_count (ref 2))

; number of SUV
(def suv_count (ref 2))

;increment car count if the total sum of car and suv is less than 5
(def increment_car (Thread. (fn []
                        (dosync
                        ;ensure the read value of suv count is consistent
                        (if (< (+ (deref car_count) (ensure suv_count)) 5) ; sum of (cars + suv) <=5
                          (alter car_count inc))))))

;increment suv count if the total sum of car and suv is less than 5
(def increment_suv (Thread. (fn []
                     (dosync
                       ;ensure the read value of car count is consistent
                       (if (< (+ (ensure car_count) (deref suv_count)) 5) ; sum of (cars + suv) <=5
                         (alter suv_count inc))))))

(doseq [p [increment_car increment_suv]] (.start p))
(doseq [p [increment_car increment_suv]] (.join p))

(if (> (+ (deref car_count) (deref suv_count)) 5)
  (println "write skew detected"))
(if (<= (+ (deref car_count) (deref suv_count)) 5)
  (println "no write skew detected")) ;