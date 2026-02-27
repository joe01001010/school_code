; Q1
(defun my-sum (L)
    (if (null L)
        0                          ; base case for it L is null return 0 because the sum of nothing is 0
        (+ (car L)                 ; add the first element of L
            (my-sum (cdr L)))))    ; call my-sum again with the reamaining elements of the list

; Q2
(defun my-max (L)
    (if (null (cdr L))             ; base case for if there is only one element return that element
        (car L)
        (max (car L)               ; if there is more than once compare the first element
            (my-max (cdr L)))))    ; call my-max with the rest of L

; Q3
(defun my-evens (L)
    (cond
        ((null L) nil)                          ; base case, if L is empty return nil
        ((evenp (car L))                        ; Check if first element of L is even
            (cons (car L)                       ; if it is even add it to the return values
                (my-evens (cdr L))))            ; process the rest of the list with except the first element
        (t (my-evens (cdr L)))))                ; if number isnt even call my-evens with the rest of the list

; Q4
(defun my-palindrome? (L)
    (cond
        ((null L) T)                            ; Check if the list is empty, if so return T
        ((null (cdr L)) T)                      ; Check if there is only one letter, if so return T
        ((eql (car L) (car (last L)))           ; Check if the first and last character of L are the same
            (my-palindrome? (butlast (cdr L)))) ; If the first and last characters are the same then call my-palindrome with the middle of L
        (t nil)))                               ; If not return nil

; Q5
(defun my-count-numbers (x)
    (cond
        ((null x) 0)                         ; If x is null return 0
        ((atom x)                            ; Checks if x is not a list
            (if (numberp x) 1 0))            ; if its a number it gets counted return 1, else return 0
    (t (+ (my-count-numbers (car x))         ; if x isnt null and is a list then get the first element and call my-count-numbers
        (my-count-numbers (cdr x))))))       ; Call my-count-numbers with the rest of the list

; Q6 a
(defun my-map (f L)
    (if (null L)
        nil                                         ; base case for if L is empty
        (cons (funcall f (car L))                   ; apply f to the first element of L and build a new list
        (my-map f (cdr L)))))                       ; call my-map with the rest of the list

; Q6 b
(defun my-filter (p L)
    (if (null L)
        nil                                         ; base case for if L is empty
        (if (funcall p (car L))                     ; sends the first element of L to function p
            (cons (car L) (my-filter p (cdr L)))    ; if true construct a new list with first element of L and call the rest of my-filter
            (my-filter p (cdr L)))))                ; if false call my-filter without adding to new list

; BONUS a
(defun my-compose (f g)
    (lambda (x)                      ; Creates arbitrary function that takes a single argument
        (funcall f (funcall g x))))  ; uses funcall to call f with the argument funcall that calls g with argument x

; BONUS b
(defun my-partial (f a)
    (lambda (x)           ; Creates arbitrary function that takes a single argument
        (funcall f a x))) ; Uses funcall to call original function f with a and x as the arguments


(print "my-sum in: (1,2,3,4), out:")
(princ (my-sum `(1,2,3,4)))
(print "my-sum in: (), out:")
(princ (my-sum `()))
(print "my-sum in: (-1,0,11,24,-24), out:")
(princ (my-sum `(-1,0,11,25,-24)))
(print "my-sum in: (1,2,3,4,05,06), out:")
(princ (my-sum `(1,2,3,4,05,06)))
(fresh-line)

(print "my-max in: (4,9,2,7), out:")
(princ (my-max `(4,9,2,7)))
(print "my-max in: (), out:")
(princ (my-max `()))
(print "my-max in: (100,1000,1000,0), out:")
(princ (my-max `(100,1000,1000,0)))
(print "my-max in: (-1,-2,-3,-4,0), out:")
(princ (my-max `(-1,-2,-3,-4,0)))
(fresh-line)

(print "my-evens in: (1,2,3,4,5,6), out:")
(princ (my-evens `(1,2,3,4,5,6)))
(print "my-evens in: (), out:")
(princ (my-evens `()))
(print "my-evens in: (-2,-4,-3,2,4,3), out:")
(princ (my-evens `(-2,-4,-3,2,4,3)))
(print "my-evens in: (0,0,0,2,2,2,3,3,3), out:")
(princ (my-evens `(0,0,0,2,2,2,3,3,3)))
(fresh-line)

(print "my-palindrome? in: (r a d a r), out:")
(princ (my-palindrome? `(r a d a r)))
(print "my-palindrome? in: (1 2 3), out:")
(princ (my-palindrome? `(1 2 3)))
(print "my-palindrome? in: (), out:")
(princ (my-palindrome? `()))
(print "my-palindrome? in: (1), out:")
(princ (my-palindrome? `(1)))
(fresh-line)

(print "my-count-numbers in: x, out:")
(princ (my-count-numbers 'x))
(print "my-count-numbers in: (x 3), out:")
(princ (my-count-numbers '(x 3)))
(print "my-count-numbers in: ((1 2) 3), out:")
(princ (my-count-numbers '((1 2) 3)))
(print "my-count-numbers in: ((a (1 b)) (2 3)), out:")
(princ (my-count-numbers '((a (1 b)) (2 3))))
(fresh-line)

(print "my-map in: (lambda (x) (* x x)) on (1 2 3 4), out: ")
(princ (my-map #'(lambda (x) (* x x)) '(1 2 3 4)))
(print "my-map in: 1+ (5 6 7), out: ")
(princ (my-map #'1+ '(5 6 7)))
(print "my-map in: () (), out: ")
(princ (my-map () ()))
(print "my-map in: 1+ (), out: ")
(princ (my-map #'1+ '()))
(fresh-line)

(print "my-filter in: oddp (1 2 3 4 5), out: ")
(princ (my-filter #'oddp '(1 2 3 4 5)))
(print "my-filter in: (lambda (x) (> x 3)) (1 2 3 4 5), out: ")
(princ (my-filter #'(lambda (x) (> x 3)) '(1 2 3 4 5)))
(print "my-filter in: (lambda (x) (< x 0)) (0 -1 -2 -02 1), out: ")
(princ (my-filter #'(lambda (x) (< x 0)) '(0 -1 -2 -02 1)))
(fresh-line)

(print "my-compose in: 5+ (lambda (x) (* x 34)), out: ")
(princ (funcall (my-compose #'1+ (lambda (x) (* x 34))) 2))
(fresh-line)

(print "my-partial in: (funcall (my-partial (lambda (a b) (and a b)) t) t), out: ")
(princ (funcall (my-partial (lambda (a b) (and a b)) t) t))
(fresh-line)