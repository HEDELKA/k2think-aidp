require('dotenv').config();
const K2ThinkClient = require('./client');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

class K2ConsoleAgent {
  constructor() {
    this.client = new K2ThinkClient({
      email: process.env.K2THINK_EMAIL,
      password: process.env.K2THINK_PASSWORD
    });
    this.conversationHistory = [];
    this.maxRetries = 2;
  }

  async executeCode(code, language = 'javascript') {
    try {
      let result;
      if (language === 'javascript') {
        result = await this.executeJavaScript(code);
      } else if (language === 'python') {
        result = await this.executePython(code);
      } else if (language === 'bash') {
        result = await this.executeBash(code);
      }
      return { success: true, output: result };
    } catch (error) {
      return { success: false, error: error.message, output: error.toString() };
    }
  }

  async executeJavaScript(code) {
    const tempFile = path.join('/tmp', `code_${Date.now()}.js`);
    fs.writeFileSync(tempFile, code);
    const { stdout, stderr } = await execAsync(`node ${tempFile}`, { timeout: 5000 });
    fs.unlinkSync(tempFile);
    return stdout || stderr;
  }

  async executePython(code) {
    const tempFile = path.join('/tmp', `code_${Date.now()}.py`);
    fs.writeFileSync(tempFile, code);
    const { stdout, stderr } = await execAsync(`python3 ${tempFile}`, { timeout: 5000 });
    fs.unlinkSync(tempFile);
    return stdout || stderr;
  }

  async executeBash(code) {
    const { stdout, stderr } = await execAsync(code, { timeout: 5000 });
    return stdout || stderr;
  }

  cleanResponse(text) {
    return text
      .replace(/<think>[\s\S]*?<\/think>/g, '')
      .replace(/<answer>([\s\S]*?)<\/answer>/g, '$1')
      .replace(/^[\s\n]+|[\s\n]+$/g, '');
  }

  extractCodeBlocks(text) {
    const codeBlockRegex = /<><\/([a-z]+)>([\s\S]*?)<\/><\/>/g;
    const blocks = [];
    let match;
    while ((match = codeBlockRegex.exec(text)) !== null) {
      blocks.push({
        language: match[1],
        code: match[2].trim()
      });
    }
    return blocks;
  }

  async processModelResponse(response) {
    const codeBlocks = this.extractCodeBlocks(response);
    const results = [];

    for (const block of codeBlocks) {
      console.log(`\n[Executing ${block.language}]`);
      const result = await this.executeCode(block.code, block.language);
      results.push(result);

      if (!result.success) {
        console.log(`[Error: ${result.error}]`);
      } else {
        console.log(`[Output]\n${result.output}`);
      }
    }

    return results;
  }

  async chat(userMessage, retryCount = 0) {
    this.conversationHistory.push({
      role: 'user',
      content: userMessage
    });

    const systemPrompt = `You are a helpful coding assistant. When providing code, use this format:
<><language>
code here
</></language>

Supported languages: javascript, python, bash

Execute code and handle errors gracefully. Always provide working solutions.`;

    try {
      const response = await this.client.chat.completions.create({
        model: 'MBZUAI-IFM/K2-Think',
        messages: [
          { role: 'system', content: systemPrompt },
          ...this.conversationHistory
        ]
      });

      const assistantMessage = response.choices[0].message.content;
      this.conversationHistory.push({
        role: 'assistant',
        content: assistantMessage
      });

      const cleanedMessage = this.cleanResponse(assistantMessage);
      console.log('\n[Assistant]');
      console.log(cleanedMessage);

      const executionResults = await this.processModelResponse(assistantMessage);

      const hasErrors = executionResults.some(r => !r.success);
      if (hasErrors && retryCount < this.maxRetries) {
        const errorSummary = executionResults
          .filter(r => !r.success)
          .map(r => r.error)
          .join('; ');

        console.log(`\n[Retrying due to errors: ${errorSummary}]`);
        return this.chat(`Previous code failed with: ${errorSummary}. Please fix it.`, retryCount + 1);
      }

      return { success: !hasErrors, results: executionResults };
    } catch (error) {
      console.error('API Error:', error.message);
      throw error;
    }
  }

  async interactiveMode() {
    const readline = require('readline');
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const question = (prompt) => new Promise(resolve => rl.question(prompt, resolve));

    console.log('K2 Console Agent (type "exit" to quit)');
    console.log('Commands: write code, execute tasks, ask questions\n');

    while (true) {
      const userInput = await question('You: ');
      if (userInput.toLowerCase() === 'exit') {
        console.log('Goodbye!');
        rl.close();
        break;
      }

      try {
        await this.chat(userInput);
      } catch (error) {
        console.error('Error:', error.message);
      }
      console.log('\n---\n');
    }
  }
}

async function main() {
  const agent = new K2ConsoleAgent();

  const command = process.argv[2];
  if (command === 'interactive') {
    await agent.interactiveMode();
  } else {
    const userMessage = process.argv.slice(2).join(' ');
    if (!userMessage) {
      console.log('Usage: node agent.js "your command" or node agent.js interactive');
      process.exit(1);
    }
    await agent.chat(userMessage);
  }
}

main().catch(console.error);
