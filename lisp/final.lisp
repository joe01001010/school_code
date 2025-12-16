(defun transform-and-sum (L f g)
    (let ((sum 0))
        (dolist (x L sum)             ; iterate over each element, return sum at end
            (let ((y (funcall f x)))    ; apply f to x
                (when (funcall g y)       ; check g
                    (incf sum y))))))       ; add to sum if true

(print (transform-and-sum '(1 2 3 4 5)
    #'(lambda (x) (* x 2))
    #'(lambda (y) (> y 5))))