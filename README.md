# SVD-image-compression

- Converts an image into 3 Matrices for Red, Green and Blue pixel values
- Applies the single value decomposition to each of them.
- Reassembles them iteratively using increasingly more of the single values into a folder called animation

Run the following to make a pretty gif
```
python con.py # run the python program
convert -delay 20 -loop 0 animation/*.jpg svd.gif # convert the frames to a gif
```
