# How to set up Typst locally
## Installation
### TL;DR
In the terminal:
- Linux: ```sudo snap install typst```
- MacOS: ```brew install typst```

In VS Code:
- Install [Tinymist Typst](https://marketplace.visualstudio.com/items?itemName=myriad-dreamin.tinymist)
- Install [vscode-pdf](https://marketplace.visualstudio.com/items?itemName=tomoki1207.pdf)

### Details
You first have to install the Typst compiler.
The simplest way to do this is by using a package manager.

On **Linux**, you can install Typst through Snap:
```
sudo snap install typst
```

On **MacOS**, you can install Typst through [Homebrew](https://brew.sh/):
```
brew install typst
```

This will allow you to use the CLI to compile `.typ` files into full documents.

To preview your changes in real time, you can use the [Tinymist Typst extension in VS Code](https://marketplace.visualstudio.com/items?itemName=myriad-dreamin.tinymist).

## Previewing and Saving Documents
With Tinymist installed, when you open a `.typ` file, you can click the preview icon in the top right (the one with the magnifying glass) or use the shortcut **Ctrl+K V** to open a live preview of what you document will look like once compiled.

By clicking the icon that appears in the top right when you're in the preview tab, you can **eject the preview**, which will open it up in a new tab in your browser instead.
I recommend doing this because the preview in VS Code can start lagging very quickly.
On my system, it became tedious to navigate and edit after just a page, whereas in the browser I had no issues with 80+ pages.

To compile your document into a PDF file, click the corresponding icon in the top right of the editor. The file will be saved to the same directory the `.typ` file is in. To view it in VS Code, you will have to install an extension like [vscode-pdf](https://marketplace.visualstudio.com/items?itemName=tomoki1207.pdf)


## Additional Resources
For a tutorial and reference on the Typst markup language, check out the [Typst Docs](https://typst.app/docs/).

[Typst GitHub Repo](https://github.com/typst/typst)

[Tinymist GitHub Repo](https://github.com/Myriad-Dreamin/tinymist)