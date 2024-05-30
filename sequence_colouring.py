#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:50:18 2024

@author: chris
"""

import matplotlib.pyplot as plt
# from matplotlib.transforms import Bbox
# from matplotlib.patches import draw_bbox
import argparse
from pathlib import Path
import os

plt.rcParams["font.family"] = "monospace"

def read_fasta(file, line_wrap, beginning, end):
    '''
    read a fasta file

    Parameters
    ----------
    file : str
        fasta file.
    line_wrap : int
        how many letters to display on a single line

    Returns
    -------
    seq : str
        sequence in the fasta file as a single string.
    lines_out : list
        list of lists of seq wrapped to line_wrap. 
        eg. seq = "qwertyuiopasdfgh" with line_wrap = 10 becomes:
            [["qwertyuiopa"],["sdfgh"]]

    '''
    
    if os.path.splitext(file)[1]!='.fasta':
        raise TypeError('Programme only works with fasta files')

    with open(file) as f:
        lines = f.readlines()
        
    clean_lines = []
    for line in lines[1:]:
        if '>' in line:
            print('Can only handle one sequence at a time. Will only use the first in the file')
            break
        
        clean_lines.append(line.strip())
    
    seq = ''.join(clean_lines)
    
    if (beginning is not None) and (end is not None):
        seq = seq[beginning-1:end-1] #correct for 1 based residue indexing here
    
    lines_out = [seq[x:x + line_wrap] for x in range(0, len(seq), line_wrap)]

    return seq, lines_out
        
def make_colour_list(seq, colour_dict, line_wrap,
                     lower=None, upper=None,
                     in_seq_colour=None, out_of_seq_colour=None):
    '''
    
    make a list of colour
    
    Parameters
    ----------
    seq : TYPE
        DESCRIPTION.
    colour_dict : TYPE
        DESCRIPTION.
    lower : int, optional
        lower limit for subsequence to be coloured. The default is None.
    upper : int, optional
        upper limit for subsequence to be coloured. The default is None.
    in_seq_colour : str, optional
        colour string for a particular sequence to be coloured. The default is None.
    out_of_seq_colour : str, optional
        colour string for anything not in (lower,upper) subsequence to be coloured. The default is None.

    Returns
    -------
    colours : list
        list in of lists in wrapped sequence shape containing each colours

    '''
    
    colors = []
    for i,j in enumerate(seq):
        if (lower is not None) and (upper is not None):
            if i in range(lower, upper):
                if in_seq_color is not None:
                    colors.append(in_seq_color)
                else:
                    colors.append(cols[j])
            else:
                colors.append(out_of_seq_color)
        else:
            colors.append(cols[j])
    
    #wrap the colours in the same way as the list
    colors = [colors[x:x + line_wrap] for x in range(0, len(colors), line_wrap)]

    return colors

def make_fig(lines_out, colours, file_name, line_wrap, count = 0,
             save_transparent=False, numbers=True
             ):
    '''
    Make the figure of highlight sequence
    
    Initially writing the wrapping for the figure needed careful definition
    of the bbox for the output, but in the end it didn't. This functionality
    left commented here in case it breaks again

    Parameters
    ----------
    lines_out : list 
        list of lists of the input sequence
    colours : list
        list of lists of the colours to annotate the sequence with.

    Returns
    -------
    None.

    '''
    fsize = 40 #fontsize

    fig, ax = plt.subplots(figsize = (1,1))
    # bboxes = []

    # count = 0
    
    #do the very first one
    text = ax.text(0, .5, lines_out[0][0], color = colours[0][0],
                   fontsize = fsize, weight = 'bold')
    # a = text.get_window_extent().transformed(ax.transData.inverted())
    # bboxes.append(np.round([a.xmin, a.xmax, 
    #                         a.ymin, a.ymax],3))
    start = text
    
    count+=1
    if numbers:
        ax.annotate(f'{count} ',
                    xycoords = text,
                    xy = (0,0),
                    va = 'bottom',
                    ha = 'right',
                    color = '#262626',
                    fontsize = fsize,
                    weight = 'bold'
                )
    
    #do the rest of the first line
    for i,j in enumerate(lines_out[0][1:],1):
        text = ax.annotate(j,
                           xycoords = text,
                           xy = (1,0),
                           va = 'bottom',
                           color = colours[0][i],
                           fontsize = fsize,
                           weight = 'bold')
        # a = text.get_window_extent().transformed(ax.transData.inverted())
        # bboxes.append(np.round([a.xmin, a.xmax, 
        #                         a.ymin, a.ymax],3))
        
        count+=1
        
    #do the remaining lines
    for i, j in enumerate(lines_out[1:],1):
        #do the first character of the line
        text = ax.annotate(j[0],
                           xycoords=start,
                           xy=(0,0),
                           va='top',
                           color = colours[i][0],
                           fontsize = fsize,
                           weight = 'bold')
        start = text
        count+=1
        if numbers:
            ax.annotate(f'{count}  ',
                        xycoords = text,
                        xy = (1,0),
                        va = 'bottom',
                        ha = 'right', 
                        color = '#262626',
                        fontsize = fsize,
                         weight = 'bold'
                        )

        # a = text.get_window_extent().transformed(ax.transData.inverted())
        # bboxes.append(np.round([a.xmin, a.xmax, 
        #                         a.ymin, a.ymax],3))
        #do the rest of the line
        for k,l in enumerate(j[1:],1):
            text = ax.annotate(l,
                               xycoords = text,
                               xy = (1,0),
                               va = 'bottom',
                               color = colours[i][k],
                               fontsize = fsize,
                               weight = 'bold')
    
            # a = text.get_window_extent().transformed(ax.transData.inverted())
            # bboxes.append(np.round([a.xmin, a.xmax, 
            #                         a.ymin, a.ymax],3))
            
            count+=1

    # lims = [[min([x[0] for x in bboxes]),
    #         min([x[2] for x in bboxes])],
    #         [max([x[1] for x in bboxes]),
    #         max([x[3] for x in bboxes])],
    #         ]
    
    # ax.set_xlim(lims[0][0], lims[1][0])
    # ax.set_ylim(lims[0][1], lims[1][1])
    ax.axis('off')
    # plt.show()
    fig.savefig(file_name,
                bbox_inches = 'tight',
                # bbox_inches = Bbox([[0,0],[1,1]]),
                dpi = 100,
                # transparent = save_transparent
                )
    # plt.close(fig)
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Make a coloured picture of a sequence in a fasta file')
    #some basic input arguments
    parser.add_argument("-f", dest="fasta", type=Path, required=True, help="Input fasta file")
    parser.add_argument("-n", dest="line_wrap", type=int, default = 10,
                        help="Number of characters of the sequence to print on a single line")
    parser.add_argument("-c", dest='numbers', default = True, action = 'store_false',
                        help="Add sequence numbering to the image")
    parser.add_argument("-b", dest='beginning', type=int, default=None,
                        help="First resid to print to image")
    parser.add_argument("-e", dest='end', type=int, default=None,
                        help="Last resid to print to image")
    

    #some stuff about how to save the image
    parser.add_argument("-t", dest="save_transparent", default=False, action='store_true',
                        help="Save picture with transparent background")
    parser.add_argument("-o", dest="out_name", type=Path, required=True,
                        help="Name of output file")
    
    #some stuff about how to highlight a particular subsequence
    parser.add_argument('-l', dest='lower', type = int,
                        help='First resid to colour in a special selection', default = None)
    parser.add_argument('-u', dest='upper', type = int,
                        help='Last resid to colour in a special selection', default = None)
    
    args = parser.parse_args()    
    
    yellow = '#F5ED51'
    red = '#F5331A'
    blue = '#4E7AF5'
    gold = '#F4B94A'
    green = '#63F46E'
    
    cols = {'F': yellow, 'W': yellow, 'Y': yellow,
            'D': red, 'E': red,
            'R': blue, 'H': blue, 'K': blue,
            'A': gold, 'G': gold, 'I': gold, 'L': gold, 'M': gold, 'P': gold, 'V': gold,
            'C': green, 'N': green, 'Q': green, 'S': green, 'T': green}
    
    out_of_seq_color = '#332D28'
    in_seq_color = '#4CC8D9'
    
    seq, lines_out = read_fasta(args.fasta, args.line_wrap, 
                                args.beginning, args.end)
    
    #correct the lower and upper annotations if beginning and end have been given
    if (args.beginning is not None) and (args.end is not None):
        lower = args.lower - 1 - args.beginning - 1 
        upper = args.upper - 1 - args.beginning - 1
        count = args.beginning - 1
    else:
        count = 0
        if (args.lower is not None) and (args.upper is not None):
            lower = args.lower - 1
            upper = args.upper - 1
        else:
            lower = None
            upper = None
    
    colours = make_colour_list(seq, cols, args.line_wrap, 
                               lower=lower, upper = upper,
                              )
    
    make_fig(lines_out, colours, args.out_name, args.line_wrap, 
             save_transparent=args.save_transparent, numbers=args.numbers,
             count = count)

