const fs = require("fs");
const readLine = require("node:readline");

const rl = readLine.createInterface({
  input: process.stdin,
  output: process.stdout,
});

try {
  rl.question("Enter the filename you wish to parse: ", (file) => {
    fs.readFile(file, "utf8", (err, data) => {
      if (err) {
        console.error(err);
        return;
      }
      try {
        console.log(JSON.parse(data));
        console.log("\n\nExiting with code: 0");
      } catch (err) {
        console.log(`${data}\n${err.message}\n\nExiting with code: 1`);
      }
    });
  });
} catch (e) {
  console.error(e);
}
