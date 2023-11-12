# Docker NS1 Dynamic DNS
This updates DNS records in NS1 with the current IP (from [ipify.org](https://www.ipify.org)) every 5 minutes. The script runs under `cron` inside a lightweight Alpine-based Docker container.

[NS1](https://ns1.com) is a DNS provider that offers a generous free plan (500k queries/month, 50 records) and an API.

## Add-on Configuration 
```
  - zone: example.com
    api-key: API_KEY
    records-to-update: [ "something.example.com", "other.exmaple.com" ]
```

