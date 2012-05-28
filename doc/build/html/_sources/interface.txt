.. _cheat-sheet:

******************
Sphinx cheat sheet
******************

Here is a quick and dirty cheat sheet for some common stuff you want
to do in sphinx and ReST.  You can see the literal source for this
file at :ref:`cheatsheet
-literal`.
   

.. _formatting-text:

Formatting text
===============

You use inline markup to make text *italics*, **bold**, or ``monotype``.

You can represent code blocks fairly easily::

   import numpy as np
   x = np.random.rand(12)

Or literally include code:

.. literalinclude:: pyplots/ellipses.py

.. _making-a-table:
====================  ==========  ==========
Header row, column 1  Header 2    Header 3
====================  ==========  ==========
body row 1, column 1  column 2    column 3
body row 2            Cells may span columns
====================  ======================


.. _making-a-table:

Split / Process / Merge
==============

Actions are simple Ruby classes that inherit from CloudCrowd::Action, and implement at least a process method, for running the parallel portion of a task.

=======     ==========   ==========================================================================================================================================================================================================================================================================================================================================
name        require      description
=======     ==========   ==========================================================================================================================================================================================================================================================================================================================================
split	    optional	 A method that uses t he input — the input being anything JSON-serializable, or a URL to a file — and splits it up into work units suitable for parallel processing. Return an array of output from this method, and each element in the array will be sent as the input to the next step (process), in parallel across all your workers.
process	    mandatory	 Perform the parallel portion of the computation. The input comes directly from your Job request, or, if you have a split method defined, from the output of split. The return value from process is either returned as the output of the job, or sent to merge for further processing.
merge	    aoptional	 The input is an unordered array of all the outputs from the process stage. The return value of merge is the result of the Job.
=======     ==========   ==========================================================================================================================================================================================================================================================================================================================================