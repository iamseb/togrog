from twisted.scripts import twistd
from togrog.utils import autoreload

autoreload.main(twistd.run)
