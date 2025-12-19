from finance.principal import Principal
from finance.rate import Rate
from finance.time import Time
from finance.interest import calculate_simple_interest

p = Principal(10000)
r = Rate(5)
t = Time(2)

si = calculate_simple_interest(p.amount, r.rate, t.time)

print("Simple Interest:", si)
