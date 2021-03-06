from pudzu.charts import *
from pudzu.dates import *

df = pd.read_csv("datasets/timeline_jerusalem.csv").split_columns("type", "|")

START, END = -2000, 2000
INTERVAL = 500
COLORS = { "christian": "#e41a1c", "pagan": "#ff7f00", "jewish": "#377eb8", "muslim": "#4daf4a" }
PHOTOS = ["https://media2.s-nbcnews.com/j/newscms/2017_20/2001786/170516-western-wall-mn-1100_9029fb3cafb1eb2f3a65fbb066ddbc0e.nbcnews-ux-2880-1000.jpg", "https://1gr.cz/fotky/idnes/15/041/org/HIG5a5131_04.jpg", "http://www.hexapolis.com/wp-content/uploads/2014/07/Dome-of-the-Rock_1.jpg"]

def stripes(colors): return Image.from_column([Image.new("RGBA", (100, 4), c) for c in colors])

def labelfn(d, w): # hack to handle 500 year cutoffs
    if "Herod" in d['period'] and w < 50: return " "
    elif "Achaemenid" in d['period'] and w < 200: return "7→"
    elif "Fatimid" in d['period'] and w < 100: return "25→"
    elif "Mamluk" in d['period'] and w < 50: return "32"
    return d['period'].replace("\\n", "\n")
    
colorfn = lambda d, w, h: Image.from_pattern(stripes([COLORS[t] for t in d['type']]), (w, h))
labeld = {frozenset({TimeChartLabelPosition.ABOVE, TimeChartLabelPosition.INSIDE, TimeChartLabelPosition.BELOW}): labelfn,
          TimeChartLabelPosition.ABOVE: lambda: " ", TimeChartLabelPosition.BELOW: lambda: " "}
data = [df.filter_rows("start<{} and end>{}".format(start+INTERVAL, start)).update_columns(start=lambda v: v-start, end=lambda v: v-start) for start in range(START, END, INTERVAL)]
llabels = ["{} BC".format(-start) if start< 0 else "AD {}".format(start+int(start==0)) for start in range(START, END, INTERVAL)]
chart = time_chart(800, 40, data, "start", "end", colorfn, interval_label_key=labeld, label_font=arial(10), 
                   xmin=0, xmax=INTERVAL, grid_font=arial(10), grid_labels=lambda v: "+{}".format(v), grid_interval=100, labels_left=llabels).pad(2, bg="black")

# Title, etc

images = Image.from_column([Image.from_url_with_cache(u).crop_to_aspect(320,200).resize((320,200)) for u in PHOTOS], bg="black")

def box(t): return Image.new("RGBA", (20,20), COLORS[t])
def label(s): return Image.from_text(s, arial(12), fg="white", bg="black")

footer = Image.from_row([
    Image.from_text("ruling entity by religion: ", arial(12, bold=True), fg="white"),
    box("pagan"), label("pagan"), box("jewish"), label("Jewish"), box("christian"), label("Christian"), box("muslim"), label("Muslim"),
    Image.new("RGBA", (50,0), 0),
    Image.from_text("* also claimed (but not controlled) by the State of Palestine", arial(12), fg="white"),
    ], padding=3, bg="black")
    
title = Image.from_column([
    Image.from_text("Jerusalem: 40 states in 4000 years".upper(), arial(36, bold=True), fg="white", bg="black"),
    Image.from_text("a political timeline of the Holy City, based on http://qr.ae/TbcqnX", arial(24), fg="white", bg="black")
    ], bg="black")

img = Image.from_column([title, Image.from_row([chart, images], bg="black", padding=5), footer], bg="black", padding=(0,10))
img.place(Image.from_text("/u/Udzu", font("arial", 12), fg="white", bg="black", padding=3).pad((1,1,0,0), "white"), align=1, padding=(5,10), copy=False)
img.save("output/timeline_jerusalem.png")
