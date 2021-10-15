from pylsl import StreamInfo, StreamOutlet


class marker:
    def __init__(self, name="my_marker"):
        self.name = name
        info_key= StreamInfo(name=self.name, type='Markers', channel_count=1,
                        channel_format='string', source_id='markerID')
        self.outlet_key = StreamOutlet(info_key)

    def stream_marker(self, _marker):
        if (_marker):
            self.outlet_key.push_chunk([str(_marker)])