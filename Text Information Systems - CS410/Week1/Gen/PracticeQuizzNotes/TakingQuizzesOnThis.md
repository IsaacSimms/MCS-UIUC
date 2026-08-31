# Misc Note(s) on taking a quiz for this topic. 
bit vector  = this part is concerned with is the term from the query present in the doc (1 for present, 0 for not)

dot product = taking the result of bit vector, multiply matching coordinates between query and doc, then adding the products. 

### L2 Distance equation:
$\|v_1 - v_2\|_2 = \sqrt{\sum_i (v_{1i}-v_{2i})^2}$
This function measures the distance between two points. Longer docs = longer tf counts, longer vectors, and the point is further from the origin. 
Two docs can have the same term proportions but lengths that are far apart **affected by vector length**

### Cosine equation:
$\cos(v_1,v_2) = \dfrac{v_1\cdot v_2}{\|v_1\|\,\|v_2\|}$
The dot product is divided by both lengths. Scaling a vector (by making the doc longer through repeating the same mix) cancels out. Length does not effect the cosine equation. 
More stable and default in Vector Space Models.
