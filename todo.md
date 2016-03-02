* [ ] Parse workouts from .wkt format
    * [x] Stream lines from a file
    * [x] Save & load JSON
        * [x] Custom JSON encoding
    * [ ] Sort Workouts by timestamp
        * [x] Serialize Workout timestamp to string
        * [x] Process timestamps in Workouts.upgrade()
* [x] CI
    * [x] Remove TravisCI job
    * [x] Create Dockerfile
    * [x] Fix Wercker job
* [ ] Parse Exercises
    * [ ] Parse string & list of strings into Workout object
    * [ ] Parse exercises from string or list of strings
    * [ ] Output as JSON
* [ ] Parse Sets
    * [ ] Parse set from string
    * [ ] Output as JSON
    * [ ] Handle shorthand notation for same weight|reps
    * [ ] Handle special set types (rest/pause, giant sets)
