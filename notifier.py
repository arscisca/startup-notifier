import socket
import urllib.request
import json
import pushover


def read_token(ftoken):
    # Set the correct path
    with open(ftoken, 'r') as f:
        return f.readline().strip()


if __name__ == '__main__':
    # Acquire information about the device
    # Public ip
    ipify_token = read_token('.ipify-token')
    url = "https://geo.ipify.org/api/v1?apiKey={api_key}".format(api_key=ipify_token)
    request = urllib.request.urlopen(url).read().decode('utf8')
    ipdata = json.loads(request)
    # Local information
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    # Send notification
    title = "Startup Notifier: '{dev}' is onnline".format(dev=hostname)
    message = "{dev} is online and connected with IP {ip_pub}, localized in {city}, {country} ({lat} N, {long} E)." \
        .format(dev=hostname,ip_pub=ipdata['ip'], city=ipdata['location']['city'],
                country=ipdata['location']['country'], lat=ipdata['location']['lat'], long=ipdata['location']['lng'])

    po_client = pushover.Client(config_path='.pushoverrc')
    po_client.send_message(message, title=title, timestamp=True)
