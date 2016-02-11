import util


DATABASE_CONNECT = {
    'redshift': {
        'ENGINE': 'redshift',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': '<instance>.us-east-1.redshift.amazonaws.com',
        'PORT': 5439,
    },
}

S3_BUCKETS = {
    'datahacks': {
        'access_key': '<access-key>',
        'secret_key': '<secret-key>',
        'path': 's3://datahacks/',
    },
}

def create_connect(server, db, schema=None):
    connect_info = dict(DATABASE_CONNECT[server].items() + {'DB': db}.items())
    if schema:
        return dict(connect_info.items() + {'SCHEMA': schema}.items())

    return connect_info



IPYTHON = util.Bunch(
    DATABASE=create_connect('redshift', '<redshift-db>', '<redshift-schema'),
    S3=S3_BUCKETS['datahacks'],
)
