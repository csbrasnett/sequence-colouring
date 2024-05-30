# sequence-colouring

Make quick pictures of sequences in fasta files using [matplotlib](https://matplotlib.org/)



## example

### default behaviour
`./sequence_colouring.py -f short.fasta -o example_default.png`

![default](figures/example_default.png)

### no counts

`./sequence_colouring.py -f example.fasta -o example_nocount.png -c`
![no numbers](figures/example_nocount.png)

### special highlighting

`./sequence_colouring.py -f example.fasta -o example_subseq.png -l 33 -u 56`
![full with subsequence](figures/example_subseq.png)


### only show a subsequence

`./sequence_colouring.py -f example.fasta -o example_subseq_highlight.png -l 33 -u 56 -b 32 -e 62`
![subsequence focus](figures/example_subseq_highlight.png)
