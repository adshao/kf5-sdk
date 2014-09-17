# KF5 SDK

---

## Python SDK

Single Python file without any dependences on other modules

Usage:

```python
from kf5client import Client, APIError

client = Client()
client.domain = 'your_domain'
client.key = 'your_api_shared_key'

# call API without '_' in API name
# list tickets, call API without params
result = client.ticket_list()
# view a ticket, call API with params
result = client.ticket_view(id=1)

# call API with '_' in API name
# list categories
result = client.call('forum/category_list')
# view a category
result = client.call('forum/category_view', id=1)

# catch API Error
try:
    result = client.ticket_view(id=1)
except APIError as e:
    print e
```

