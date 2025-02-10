# Contributing to Django Meilisearch integration

Thank you for considering contributing to this project! We welcome contributions from the community to help improve and expand the Django-Meilisearch integration.

## How to contribute

### 1. Fork the repository

Click the **Fork** button at the top-right corner of the repository page to create your own copy.

### 2. Clone your fork

Clone your forked repository to your local machine:

```sh
git clone https://github.com/{your_username}/django_meilisearch.git
cd django_meilisearch
```

### 3. Set up the development environment

Ensure you have Python and Poetry installed and set up a virtual environment:

```sh
poetry install
poetry shell
```

Additionally, you need to have a Meilisearch instance running. To make things easier, you can use Docker for this:

```sh
docker run --name meilisearch -p 7700:7700 --rm -d getmeili/meilisearch:latest
```

!!! note
    I use to run the container using `--rm` option to automatically remove the container when it stops, but you can ommit this option if you want to reuse the same container.

### 4. Create a new branch

Always create a new branch for your changes:

```sh
git switch -c {prefix}/{description}  # or git checkout -b {prefix}/{description} if you are using an older version of git
```

!!! warning
    We use Git Flow to manage branches with the default naming convention. Make sure to follow the naming convention for your branch. If you prefer, you can use the [Git Flow extension](https://github.com/nvie/gitflow).

| Branch type | Prefix | Example |
| --- | --- | --- |
| Feature | feature | feature/your-feature-name |
| Bugfix | fix | fix/your-bug-name |
| Hotfix | hotfix | hotfix/your-hotfix-name |

### 5. Make your changes

Modify the code, add new features, or fix bugs. Make sure to follow the existing code style.

### 6. Run tests

Before submitting a pull request, ensure all check and tests pass:

```sh
poetry run check
```

### 7. Commit and push your changes

Commit your changes and push them to your fork:

```sh
git add .
git commit -m "Your commit message"
git push origin feature/your-feature-name
```

### 8. Open a Pull Request

Go to the original repository and click the **New pull request** button. Fill in the details and submit your pull request.

!!! note
    Make sure to reference the issue you are addressing in your pull request description and to provide a detailed explanation of your changes.

## 💡 Contribution guidelines

- Make sure to follow the package's code style.
- Write tests for new features and bug fixes.
- Keep commits clean and concise.
- Update the documentation if necessary.

## 🤝 Need help?

If you have any questions or need help with anything, feel free to open an issue or reach out to the maintainers.

***Happy coding! 🚀***
