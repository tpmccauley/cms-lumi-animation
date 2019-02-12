
# coding: utf-8

# In[ ]:


# https://cern.ch/cmslumi/publicplots/lumiByDay.csv
lumi = pd.read_csv('lumiByDay.csv')
lumi.head()


# In[ ]:


lumi['Date'] = pd.to_datetime(lumi.Date)

# Run 2
min_date = pd.Timestamp(year=2015, month=6, day=3)
max_date = pd.Timestamp(year=2018, month=10, day=26)

lumi = lumi[(lumi.Date <= max_date) & (lumi.Date >= min_date)]

lumi['CMS recorded'] = lumi['Recorded(/ub)'].cumsum() / 1e9
lumi['LHC delivered'] = lumi['Delivered(/ub)'].cumsum() / 1e9

lumi.tail()


# In[ ]:


cms_orange= (0.945, 0.76, 0.157)
cms_blue = (0.0, 0.596, 0.831)

from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
import matplotlib.lines as mlines

FONT_PROPS_SUPTITLE = FontProperties(size="x-large", weight="bold", stretch="condensed")
FONT_PROPS_TITLE = FontProperties(size="large", weight="regular")
FONT_PROPS_AX_TITLE = FontProperties(size="x-large", weight="bold")
FONT_PROPS_TICK_LABEL = FontProperties(size="large", weight="bold")
DATE_FMT_STR_AXES = "%-d %b"

matplotlib.rcParams["font.size"] = 10.8 
matplotlib.rcParams["axes.labelweight"] = "bold"


# In[ ]:


for i in range(2,len(lumi)):
    
    axes = lumi[1:i].plot(x='Date', y=['LHC delivered', 'CMS recorded'], 
                   kind='area', stacked=False, figsize=(12*0.75,9*0.75), 
                   color=[cms_blue, cms_orange], alpha=1.0)
    
    axes.tick_params(axis='y', which='both', labelright=True)
    
    ylocs, ylabels = plt.yticks() 
    for label in ylabels:
        label.set_font_properties(FONT_PROPS_TICK_LABEL)
        
    xlocs, xlabels = plt.xticks() 
    for label in xlabels:
        label.set_font_properties(FONT_PROPS_TICK_LABEL)
    
    lumi_delivered = '{0:.2f}'.format(lumi[1:i]['LHC delivered'].values[-1])
    lumi_recorded = '{0:.2f}'.format(lumi[1:i]['CMS recorded'].values[-1])
    
    plt.suptitle('CMS Integrated Luminosity, pp, $\mathrm{\sqrt{s} =}$ 13 TeV', fontproperties=FONT_PROPS_SUPTITLE)
    plt.title('Data included from 2015-06-03 to 2018-10-26', fontproperties=FONT_PROPS_TITLE)

    plt.ylim(0, 180)
    plt.ylabel('Total Integrated Luminosity ($\mathrm{{fb}^{-1}}$)', fontproperties=FONT_PROPS_AX_TITLE)

    plt.xlim(min_date, max_date)
    plt.xlabel('Date', fontproperties=FONT_PROPS_AX_TITLE)
    
    cms_square = mlines.Line2D([], [], color=cms_orange, 
                               label='CMS Recorded: '+lumi_recorded+' ($\mathrm{{fb}^{-1}}$)',
                               marker='s', linestyle='None', markersize=10)
    
    lhc_square = mlines.Line2D([], [], color=cms_blue, 
                               label='LHC Delivered: '+lumi_delivered+' ($\mathrm{{fb}^{-1}}$)',
                               marker='s', linestyle='None', markersize=10)
    
    plt.legend(handles=[lhc_square, cms_square],
               loc=2, frameon=False, 
               prop={'weight':'bold', 'size':'large'})
    
    plt.savefig('./images/lumi'+str(i-1)+'.png')

