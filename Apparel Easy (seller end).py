import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('saleDetails.csv')

business = data['sales'].values

x = np.arange(len(business))

plt.plot(x+1,business,'go',linestyle='solid')

plt.title('Apparel Easy Sales')

plt.xticks(x+1)

plt.xlabel('nth sale')
plt.ylabel('Rupees')

plt.xlim(0.9)
plt.ylim(0)

plt.grid(True)

plt.show()
