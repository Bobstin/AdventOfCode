import pdb

class Page:
    def __init__(self, page: str, rules: list[str]) -> None:
        self.page = page
        self.rules = rules

    def __lt__(self, other):
        if other.page in self.rules:
            return False
        return True

    def __str__(self):
        return self.page

    def __repr__(self):
        return self.page


def load_inputs(rules_file: str, updates_file: str) -> tuple[dict[str, list[str]], list[list[str]]]:
    with open(rules_file) as f:
        rules_lines = f.readlines()
    rules: dict[str, list[str]] = {}
    for line in rules_lines:
        page_1, page_2 = line.split("|")
        page_1 = page_1.strip()
        page_2 = page_2.strip()

        if page_2 not in rules:
            rules[page_2] = []
        rules[page_2].append(page_1)

    with open(updates_file) as f:
        update_lines = f.readlines()
    update_lines = [line.strip() for line in update_lines]
    updates = [line.split(",") for line in update_lines]

    return rules, updates


def check_if_update_passes(rules: dict[str, list[str]], update: list[str]) -> bool:
    prior_pages = set()
    for page in update:
        if page in rules:
            for rule in rules[page]:
                if rule in update and rule not in prior_pages:
                    return False
        prior_pages.add(page)

    return True


def check_updates(rules: dict[str, list[str]], updates: list[list[str]]) -> tuple[list[list[str]], list[list[str]]]:
    passing_updates = []
    failing_updates = []
    for update in updates:
        update_passes = check_if_update_passes(rules, update)
        if update_passes:
            passing_updates.append(update)
        else:
            classed_update = [Page(page, rules.get(page, [])) for page in update]
            classed_update.sort()
            failing_updates.append([str(page.page) for page in classed_update])

    return passing_updates, failing_updates


def score_updates(updates: list[list[str]]) -> int:
    total_score = 0
    for update in updates:
        middle = len(update) // 2
        total_score += int(update[middle])

    return total_score


if __name__ == "__main__":
    test_rules, test_updates = load_inputs("test_rules.txt", "test_updates.txt")
    test_passing_updates, test_failing_updates = check_updates(test_rules, test_updates)
    test_score = score_updates(test_passing_updates)
    test_fail_score = score_updates(test_failing_updates)
    assert test_score == 143
    assert test_fail_score == 123

    rules, updates = load_inputs("rules.txt", "updates.txt")
    passing_updates, failing_updates = check_updates(rules, updates)
    score = score_updates(passing_updates)
    fail_score = score_updates(failing_updates)
    print(score)
    print(fail_score)
    assert score == 6034
    assert fail_score == 6305
