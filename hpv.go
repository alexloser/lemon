package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"os/exec"
	"runtime"
	"strings"
)

func OpenPipe(cmd *exec.Cmd) (stdout, stderr io.ReadCloser, err error) {
	if stdout, err = cmd.StdoutPipe(); err != nil {
		return
	}
	if stderr, err = cmd.StderrPipe(); err != nil {
		return
	}
	return
}

func Execute(command string) ([]string, error) {
	seq := strings.Split(command, " ")
	cmd := exec.Command(seq[0], seq[1:]...)
	stdout, stderr, err := OpenPipe(cmd)
	if err != nil {
		return nil, err
	}
	defer stdout.Close()
	defer stderr.Close()

	if err = cmd.Start(); err != nil {
		return nil, err
	}

	r := bufio.NewScanner(stdout)
	output := make([]string, 0)
	for r.Scan() {
		output = append(output, r.Text())
	}

	r = bufio.NewScanner(stderr)
	for r.Scan() {
		output = append(output, r.Text())
	}

	return output, nil
}

func CheckHardware() bool {
	ncore := runtime.NumCPU()
	fmt.Printf("Number CPU      : %d\n", ncore)
	if ncore < 4 {
		return false
	}
	out, err := Execute("cat /proc/cpuinfo")
	if err != nil {
		return false
	}
	for i := range out {
		if len(out[i]) <= 2 {
			break
		}
		if strings.Index(out[i], "processor") == 0 {
			continue
		}
		fmt.Println(out[i])
		if strings.Index(out[i], "model name") > 0 {
			if strings.Index(out[i], "Intel") < 0 && strings.Index(out[i], "AMD") < 0 {
				return false
			}
		} else if strings.Index(out[i], "flags") > 0 {
			if strings.Index(out[i], "sse2") < 0 || strings.Index(out[i], "sse4") < 0 {
				return false
			}
		}
	}
	fmt.Println()

	out, err = Execute("free -mht")
	if err != nil {
		return false
	}
	for i := range out {
		fmt.Println(out[i])
	}
	fmt.Println()

	out, err = Execute("df -h")
	if err != nil {
		return false
	}
	for i := range out {
		fmt.Println(out[i])
	}
	fmt.Println()

	out, _ = Execute("uname -a")
	for i := range out {
		fmt.Println(out[i])
	}
	fmt.Println()

	out, _ = Execute("lsb_release -a")
	for i := range out {
		fmt.Println(out[i])
	}
	fmt.Println()

	out, err = Execute("gcc -v")
	if err != nil {
		return false
	}
	hasGcc := false
	for i := range out {
		pos := strings.Index(out[i], "gcc version")
		if pos >= 0 {
			fmt.Println(out[i][pos:])
			hasGcc = true
			break
		}
	}
	if !hasGcc {
		fmt.Println("Can Not find gcc compiler!")
	}
	fmt.Println()

	out, err = Execute("python3 -V")
	if err != nil {
		return false
	}
	hasPy3 := false
	for i := range out {
		pos := strings.Index(out[i], "Python 3.")
		if pos == 0 {
			fmt.Println(out[i][pos:])
			hasPy3 = true
		}
	}
	if !hasPy3 {
		fmt.Println("Can Not find Python3!")
	}
	fmt.Println()

	return true
}

func main() {
	if CheckHardware() != true {
		fmt.Println("Checking Failed!")
		fmt.Println("Sorry, this computer is unable to meet demand!\n")
		os.Exit(-1)
	} else {
		fmt.Println("Checking Finished!\n")
		os.Exit(0)
	}
}
