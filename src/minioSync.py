# Access key， security is not ready

from minio import Minio
from minio.error import S3Error


class minIOC():
    def __init__(self):
        pass

    def conn(self, conf):
        self.client = Minio(**conf)

    def upload_file(self, bucket, files):
        import pdb
        pdb.set_trace()
        try:
            buckets = self.client.list_buckets()
            # self.client.list_objects("my-bucket")
            found = self.client.bucket_exists(bucket)
            if not found:
                self.client.make_bucket(bucket)
            else:
                print("Bucket {bucket} already exists")

            self.client.fput_object(files)

        except S3Error as exc:
            print("error occurred.", exc)
            


if __name__ == "__main__":
    conf = {
    'endpoint' : "192.168.13.89:9000",
    'access_key' : "admin",
    'secret_key' : "admin123",
    'secure' : False

    }
    bucket = "dev-datasets",
    files = "jinghe数据/DWD_DEFECT_CLASS_202308150937.csv",
    mc = minIOC()
    mc.conn(conf)
    mc.upload_file(bucket, files)


