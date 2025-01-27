// originally based on https://github.com/agarwalvishal/claude-chat-exporter
// hackily modified it to work with artifacts by making everything async then
// adding in .click(), async sleeping and lots of await to fetch each version of the artifact

(async function () {
    async function extractConversation() {
    let markdown = "# Conversation with Claude\n\n";
    const messages = document.querySelectorAll('.font-claude-message, .font-user-message');

    for (const message of messages) {
      const isHuman = message.classList.contains('font-user-message');
      const role = isHuman ? 'Human' : 'Claude';
      markdown += `## ${role}:\n\n`;

      const content = isHuman ? message : message.querySelector('.grid-cols-1');
      if (content) {
        markdown += await processContent(content);
      }

      markdown += "\n";
    };

    return markdown;
  }

  async function processContent(element, depth = 0) {
    let markdown = '';
    const children = element.childNodes;

    for (let child of children) {
      if (child.nodeType === Node.TEXT_NODE) {
        markdown += child.textContent;
      } else if (child.nodeType === Node.ELEMENT_NODE) {
        switch (child.tagName) {
          case 'P':
            markdown += await processInlineElements(child) + "\n\n";
            break;
          case 'OL':
            markdown += await processList(child, 'ol', depth) + "\n";
            break;
          case 'UL':
            markdown += await processList(child, 'ul', depth) + "\n";
            break;
          case 'PRE':
            const codeBlock = child.querySelector('.code-block__code');
            if (codeBlock) {
              const language = codeBlock.className.match(/language-(\w+)/)?.[1] || '';
              markdown += "```" + language + "\n" + codeBlock.textContent.trim() + "\n```\n\n";
            }
            break;
          default:
            markdown += await processInlineElements(child) + "\n\n";
        }
      }
    }

    return markdown;
  }

  async function processList(listElement, listType, depth = 0) {
    let markdown = '';
    const items = listElement.children;
    const indent = '  '.repeat(depth);

    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      const prefix = listType === 'ol' ? `${i + 1}. ` : '- ';
      elements = await processInlineElements(item)
      markdown += indent + prefix + elements.trim() + "\n";

      const nestedLists = item.querySelectorAll(':scope > ol, :scope > ul');
      for (let nestedList of nestedLists) {
        markdown += await processList(nestedList, nestedList.tagName.toLowerCase(), depth + 1);
      }
    }

    return markdown;
  }

  async function processInlineElements(element) {
    let markdown = '';
    const children = element.childNodes;

    for (let child of children) {
      if (child.nodeType === Node.TEXT_NODE) {
        markdown += child.textContent;
      } else if (child.nodeType === Node.ELEMENT_NODE) {
        if (child.tagName === 'BUTTON') {
          child.click();
          await new Promise(r => setTimeout(r, 100));
          code = document.querySelectorAll("[class^=language]");
          if (code.length) {
            code_text = code[0].textContent;
            language = code[0].className.match(/language-(\w+)/)?.[1] || '';
          } else {
            code_text = "";
            language = "unknown";
          }
          markdown += "```" + language + "\n" + code_text +  "\n```\n\n";
        } else if (child.tagName === 'CODE') {
          markdown += '`' + child.textContent + '`';
        } else if (child.tagName === 'OL' || child.tagName === 'UL') {
          // Skip nested lists here, they will be handled separately
          continue;
        } else {
          markdown += await processInlineElements(child);
        }
      }
    }

    return markdown;
  }

  function downloadMarkdown(content, filename) {
      const blob = new Blob([content], { type: 'text/markdown' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
  }

  const conversationMarkdown = await extractConversation();
  downloadMarkdown(conversationMarkdown, 'claude_conversation.md');
  })();