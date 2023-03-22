Elizabeth Akindeko

About
This was a fun python project that mimics an E20 assembler. An E20 assembler converts E20 assembly
language into E20 machine Language. Once an E20 assembly language file is inputed, the program 
will traverse the lines of code from that file and attempt to accurately convert the instructions
from each line into the machine code, and then display it.


The Making
I chose to use python to create this program because it made more sense to me than c++, as I'm not very experinced
with c++'s syntax. And since I haven't used the language for any of my projects in about a year,
I went back to my old lectures from my CS-UY1114 python class on NYU classes. Specifically, I reviewed the final
exam and my memory of the language returned.

After the project was announced I reviewd the folder and began to work on the project on the PyCharm software.
Before this, I went back to the E20 manual to review the possible operation codes that could appear in each instruction 
as well as E20 labels.

Breaking down on E20 Labels
My program has a function titled 'removeLabelsFromString' that will extract any label from each line before
continuing to read the instruction on the same line or the subsequent instruction.
A line is passed as a parameter to the function if the line has a colon in it (i.e. ':'). Once a label is extracted it
is stored into the labels dictionary. The output is a modified version of the line that no longer includes labels.

Breaking down on Instructions
Once a line has been modified to only feature an instruction(if any), the program will count how many registers
are given in the instruction by counting the number dollar signs that appear in it. In the E20 manual there 
are 3 types of instructions; 3-register, 2-register, 0-register and some other variances that 
mimic the behaviors of 3 or 2-register instructions. I used the knowledge to design how my program
will read the given instruction and interpret it.

Interpreting Instructions
I noticed in the E20 manual that though instructions may have the same amount of registers, their machine
language order vary on the operation code of the instruction. This lead to creating operation-code-specific 
conditionals in instructions so that the program could assemble the machine language accurately for that specific operation code.
For this reason the program functions 'twoRegisterHandler' and 'lineToBinaryString' may appear weak. However, since some
operation codes in E20 have a similar machine languge orders, the same method was used to interpret their instructions to
avoid redundancy. And for that reason, the program function 'threeRegisterHandler' might appear strong because it
is able to handle most of the operation codes that have 3 registers in their instructions.

String Manipulation
I learned how to use the % operatior from https://stackabuse.com/python-string-interpolation-with-the-percent-operator/
I use this operator in my functions that convert integers into some-bit binary. 
For example, in some functions that take bits as an input, I have something like:
x = '{0:0%sb}' % (bits)
binNumber = x.format(number)
which will convert an integer number into an n-bit binary, n being the input 'bits'.

I also learned how to retrieve the first nth item or the last nth item using string indexing from 
https://www.pythonforbeginners.com/basics/string-manipulation-in-python
This is used thoughout my program to extract register numbers, labels, and operation codes from a line.

Handling Immediates
Immediates in E20 can either be positive or negative numbers or labels. And so I created a function 'isImmNumNegOrALabel' to 
receive a specific input from a line and return the correcponding binary number of the input. All but 3-register handlers use
this function to convert the given immediate into appropriate binary. And a function called 'twosComplement' was created to
convert numbers into their binary complement in the given bits.

Big Revision
I had to revise my program after "completing" it without regard for undefined (or 'to be defined') labels that appear in an
instruction, and so I created a new list called 'label_restore' that will append a tuple containing an undefined label's name, 
the current address it was called in, the operation code, and how many bits the label would represent.

So whenever my 'isImmNumNegOrALabel' function receives an undefined label, it will put the label's data in a tuple and append it into 'label_restore',
returning a n-bit value of 0 in its place.

Once every line has been read, a fucntion 'restoreLabels' would work in conjuction with the data in 'label_restore' and the labels
dictionary to determine how to accurately insert the label's value into the instructions list based on the location it was referenced and 
the operation code that refrenced it (The instructions list is still in binary at this time but is afterwards converted to a list of
integers once all the labels are in place)

Conclusion
After the 'restoreLabels' function was created, the program was tested using all available files, and each time it produced a 
succesful machine language interpretation. It was also tested using some made up instructions like having 10 labels before an instruction, 
and having all negative immediates and it still displayed succesful interpretations. And so at this time, I am not aware of any bugs in
my program if there are any, but I suspect that I could have shortened my solution if I had more practice with python.

Ultimately, this improved my understanding of the E20 language.
