from rest_framework.throttling import UserRateThrottle 

class TenCallsPerMinutes(UserRateThrottle):
    scope = 'ten'