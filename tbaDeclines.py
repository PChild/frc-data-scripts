import gen

YEAR = 2018

tba = gen.setup()

hasDeclines = []

for year in range(2010, YEAR+1):
    print("\nProcessing", year)

    events = tba.events(YEAR, True, True)
    maxSize = len(events)
    currentSize = 0
    for event in events:
        currentSize += 1
        gen.progressBar(currentSize, maxSize)
        try:
            for alliance in tba.event_alliances(event):
                if alliance['declines'] != []:
                    print(event, "had declines")
                    hasDeclines.append(event)
        except:
            pass
print("There have been declines at", len(hasDeclines), "events according to TBA.")