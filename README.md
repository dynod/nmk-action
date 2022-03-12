# nmk-action
Github action to use nmk builder

## Usage

To use this action, just declare a step like this in your workflow file:
```yaml
- name: My step
  uses: dynod/nmk-action@v1
  with:
      task: tests
```

Input parameters are:

### task
Nmk task to be invoked (default: *build*)

## Available Python versions

This action embeds different Python versions, that can be used by referencing the following tags:
* **`v1-3.7`**
* **`v1-3.8`** (default, same as **`v1`**, as Python 3.8 is the default version of the oldest Ubuntu LTS version at the moment (**18.04**))
* **`v1-3.9`**
* **`v1-3.10`**
