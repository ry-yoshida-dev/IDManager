# IDManager

## Overview

Issue sequential integer IDs with a configurable start and step. `IDManager` is thread-safe, so multiple threads can share one instance without issuing duplicate IDs.

## Installation

Requires Python 3.11+.

```bash
pip install git+https://github.com/ry-yoshida-dev/IDManager.git
```

## Usage

```python
from id_manager import IDManager

manager = IDManager()
manager.next_id()  # 0
manager.next_id()  # 1

manager = IDManager(current_id=10, step=5)
manager.next_id()  # 10
manager.next_id()  # 15

manager.reset(start=100)
manager.next_id()  # 100
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

This package includes code derived from UniversalTracker, developed by RIIPS (Research Institute for Infrastructure Paradigm Shift), an in-house laboratory of Yachiyo Engineering Co., Ltd.
