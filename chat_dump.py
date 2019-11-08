import heroprotocol, sys, os, os.path, pprint
from heroprotocol.mpyq import mpyq
sys.path.append(os.path.join(os.getcwd(), "heroprotocol"))

from heroprotocol import protocol29406

archive = mpyq.MPQArchive(sys.argv[-1])

contents = archive.header['user_data_header']['content']
header = protocol29406.decode_replay_header(contents)
baseBuild = header['m_version']['m_baseBuild']
try:
    protocol = __import__('protocol%s' % (baseBuild,))
except:
    print >> sys.stderr, 'Unsupported base build: %d' % baseBuild
    sys.exit(1)

message_events = protocol.decode_replay_message_events(archive.read_file('replay.message.events'))

for message in message_events:
    if 'm_string' in message:
        print(message['m_string'])