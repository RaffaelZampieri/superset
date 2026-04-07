# docker/ssl/

Place your SSL certificate here **before** starting the stack.

## Required file

| File | Description |
|---|---|
| `server.pem` | Combined PEM file containing: **certificate chain first, then private key** |

## Format

The file must be a standard PEM-format file with both sections present:

```
-----BEGIN CERTIFICATE-----
... (your certificate, then any intermediate CA certs) ...
-----END CERTIFICATE-----
-----BEGIN PRIVATE KEY-----
... (your private key) ...
-----END PRIVATE KEY-----
```

If your certificate and key are in separate files, combine them:

```bash
cat your-cert.crt your-key.key > docker/ssl/server.pem
```

## Security

- `*.pem` and `*.key` files in this directory are **git-ignored** — they will never be committed.
- Never share or commit your private key.
- Restrict file permissions: `chmod 600 docker/ssl/server.pem`
