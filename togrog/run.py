from twisted.scripts import twistd
from mistral.utils import autoreload

autoreload.main(twistd.run)
