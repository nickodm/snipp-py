# ℹ️ About Snipp

**Snipp** is a CLI tool written in Python 3.10 to manage snippets from the terminal. You can create, edit, export, import, deploy, rename and remove snippets.

## ❓ What is a Snippet?

A snippet is a reusable atomic pack of files and directories that can be deployed to start a new project quickly.

## 🧠 The Main Idea

These are the main ideas that gave birth to **Snipp**.

### ⌛ Save Time & Energy

When you have a brilliant coding idea, you create a folder for your project, and you want to instantly start to develop the program that resolves a problem that you no longer want to deal with. But, in most cases, you end up wasting a lot of time (and energy) while writing some code that can perfectly be copy-pasted from another project (for example, Python's `argparse` structure), or you losing momentum while structuring your project according to some standards.

With **Snipp**, you can create your base project structure once, create a snippet, and then you just need to write `snipp deploy` to instantly spin up your entire project structure.

### ❌ Avoid Mistakes

Sometimes, when you have a file template and you need to use it, you duplicate the template, modify the structure, fill the placeholders and save the changes. But then, when you've just finished, you realize that you never duplicated your template, and you were modifying the original file the whole time. That's frustrating.

This doesn't happen with **Snipp**. Since a snippet is saved as a single file with the `.snipp` extension, it is **impossible** to modify your original file template by mistake.

# 🔽 Installation

If you have pip and git installed, install snipp by running the following command:

## Via pipx (recommended)

It is highly recommended to install this program using [pipx](https://github.com/pypa/pipx). To install snipp, run the following command:

```bash
pipx install git+https://github.com/nickodm/snipp-py.git@v0.1.0 # Or whatever version you want
```

## Via pip

You can also install snipp using pip, with this command:

```bash
pip install --user git+https://github.com/nickodm/snipp-py@v0.1.0 # or whatever version you want
```

## Via My Own Installer

Or, you can use my own script installer, [ndminstaller](https://github.com/nickodm/ndminstaller):

```bash
ndminstall snipp-py
```

# ✅ Usage

These are all the snipp commands:

| Command | Function |
|---------|  --- |
| create  | Create a new snippet |
| deploy  | Deploy a saved snippet |
| edit    | Edit a snippet's content |
| list    | List all the saved snippets |
| purge   | Delete all the saved snippets |
| show    | Show the information about a single snippet |
| remove  | Remove a saved snippet |
| export  | Export a snippet |
| import  | Import a snippet |
| rename  | Rename a snippet |


## Creating a Snippet

To create as snippet, use the following command:

```bash
snipp create name [-d DESCRIPTION | -D PATH] [-p PATH] [--no-git] [--save-to PATH]
```

For example:

```bash
snipp create "Name of the Snippet" -p "~/my_snippets/python_script"
```

## Deploying a Snippet

To deploy a snippet, use the following command:

```bash
snipp deploy (-n NAME | -i ID) [-p PATH] [-f]
```

For example, to deploy the snippet named "Python Script" in the directory "my_project", write this in your terminal:

```bash
snipp deploy -n "Python Script" -p "./my_project"
```

This will create all the directories inside the snippet, and will write the files and its contents.

## Editing a Snippet

To start editing a snippet's content, use the following command:

```bash
snipp edit (-n NAME | -i ID)
```

This will create a **temporary folder** to let you modify the contents of the snippet. Be careful, **do not delete your temporary files while editing your snippet, or your changes will be LOST!**

When you finish your changes, save them by running the following command:

```bash
snipp edit done
```

Or, if you don't want to save changes, you can use the following command:

```bash
snipp edit abort
```

Both of this commands will **delete the temporary folder**.
