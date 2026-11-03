#!/bin/bash
cat > hello <<'EOF'
#!/bin/bash
echo "Hello, $1!"
EOF
chmod +x hello
