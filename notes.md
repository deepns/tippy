# Notes

## Thoughts

What this is about?

- Collection of tips or things to remember
- want to show them in my radar

### Data format

starting with json. why?

- simplicity
- portability

don't have to worry about performance for now as the collection is going to be small (rare to reach even 1000 anytime soon)

data format

- description - text describing the tip
- tags - list of strings e.g. ["vscode", "linux", "grep"]
- content - actual content of the tip. list of preformatted lines
- hidden - boolean to show a tip or not
- id/uuid?? - may be not needed. the list index can be used as an implicit id for now.

Should the content support markdown?

```json
{
    "tips": [
        {
            "description" : "",
            "tags": [],
            "contents" : [],
            "enabled" : true
        }
    ]
}
```

config format

If `tags` is empty, show any tag.

```json
{
    "tags": [],
    "count": 1
}
```

### Functionality

- Pick a random tip
- Pick a random tip in the chosen tag
- number of tips to show? - determined by the config file
- config file -> save the tag type, number of tips to show, path to tip file
- cache file -> save the last shown time stamp?
- spaced repetition? (may be for future)
- timestamp
  - creation
  - last shown
- flag to show or hide (useful for tip that is well known, so it doesn't repeat)
- two separate db // may be read all json in a given path
  - personal
  - work

## Tasks

- [ ] Find how a python project is organized
- [ ] Add outline of work to do
- [ ] config file name pre-determined.
- [ ] Define the output format
- [x] a quick poc
- [ ] Start with dicts..then add custom classes
- [ ] Add UTs
- [ ] Add entries to db
- [ ] Things to read
  - [ ] [Real-Python JSON encoding/decoding](https://realpython.com/python-json/)
- [ ] JSON schema
