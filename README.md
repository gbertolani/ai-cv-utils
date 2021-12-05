# AI-CV-UTILS
## _The best tool for generating test data_

Become a test data wizard, generating data quickly and easily.

## Features

- Separate images into different folders according to percentages
- Delete background in images
- Generate scenarios with test data
- ✨ Magic ✨

## Installation

Using pip
```
pip install ai-cv-utils
```

## Usage

### Separate images into different folders according to percentages

```
aicv split <source of files> -t <train_folder> -v <validation_folder> -x <test_folder> -T <train_percent> -V <validation_percent> -X <test_percent>
```

### Delete background in images

```
aicv rmbg -s <source of files> -t <target>
```

### Generate scenarios with test data

```
aicv yologen -b <source of background> -s <samples_folder> -o <outout_folder>  -f <format_of_images> -z <percent_samples_size> -d <sample_degree_to_rotate> -q <qty_stages>
```


## Licence

ai-cv-utils is provided under a AGPL3+ license that can be found in the [LICENSE](https://github.com/gbertolani/ai-cv-utils/blob/main/LICENSE) file. By using, distributing, or contributing to this project, you agree to the terms and conditions of this license.
