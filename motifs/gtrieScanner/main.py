from wasabi import msg

from preprocessing import graph2edges
from runner import runner

#log = graph2edges('../../datasets/twitter','input/')
log = runner('input/','output/',4)