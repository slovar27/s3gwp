from flask import Flask, request, send_from_directory, send_file, abort
import boto3, os

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route("/hello")
def hello():
    return "hello"

@app.route("/health")
def health():
    return "ok"


@app.route('/path/<path:subpath>')
def dl_file(subpath):
    # show the subpath after /path/
    temp = (str(subpath)).split("/")
    file_name = temp[(len(temp) - 1)]

    list_folder = temp[:-1]

    folder = ("/").join(list_folder)
    store_path = "/tmp/data27/" + folder

    os.system("mkdir -p " + store_path)

    s3path = str(subpath)
    local_path = store_path + "/" + file_name

    print(s3path)
    print(local_path)
    bucket_name = file_read_string("/tmp/s3gw_bucket.txt")
    try:
        s3_client = boto3.client('s3')
        s3_client.download_file(bucket_name, s3path, local_path)
    except Exception as e:
        print("Exception:")
        print(str(e))
        abort(404)

    x = send_file(local_path, as_attachment=True)
    os.system("rm -rf " + store_path)
    return x


def awscred():
    access_key = os.environ['aak']
    secret_key = os.environ['ask']
    region = os.environ['areg']
    tpl_config = """
[default]
region = {region} 
"""
    config = tpl_config.replace("{region}",region)
    file_add_string('/root/.aws/config', config, "w")

    tpl_credentials = """
[default]
aws_access_key_id = {id}
aws_secret_access_key = {secret}
"""
    credentials = tpl_credentials.replace("{id}",access_key).replace("{secret}", secret_key)
    file_add_string('/root/.aws/credentials', credentials, "w")
    return "should be done"


# mode w for overwrite
def file_add_string(path, string, mode = "a"):
    with open(path, mode) as myfile:
        myfile.write(string)

def file_read_string(path):
    with open(path, "r") as myfile:
        return myfile.read()


if __name__ == "__main__":
    # prepare storage folder
    os.system("mkdir -p /tmp/data27")
    # prepare creds
    awscred()
    # store bucket name
    file_add_string("/tmp/s3gw_bucket.txt", os.environ['backetname'], "w")
    app.run('0.0.0.0','3002')