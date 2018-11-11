package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	csvFile, _ := os.Open("times_lab.csv")
	r := csv.NewReader(csvFile)
	
	tSeq, err := r.Read();
	if err != nil {
		log.Fatal(err)
	}
	tPars, err := r.ReadAll();
	if err != nil {
		log.Fatal(err)
	}
	
	// speedup
	var speedup [][]float64
	for i, tPar := range tPars {
		fmt.Print("|")
		fmt.Print(2 * (i + 1))
		fmt.Print("            |")
		var speedupI []float64
		for j := 0; j < len(tSeq); j++ {
			tSeqFloat, _ := strconv.ParseFloat(tSeq[j], 64)
			tParFloat, _ := strconv.ParseFloat(tPar[j], 64)
			speedupI = append(speedupI, tSeqFloat / tParFloat)
			fmt.Printf("%.3f", speedupI[j])
			fmt.Print("         |")
		}
		speedup = append(speedup, speedupI)
		fmt.Println()
	}
	fmt.Println()
	// efficiency
	for i := 0; i < len(tPars); i++ {
		fmt.Print("|")
		nrP := float64(2 * (i + 1))
		fmt.Print(nrP)
		fmt.Print("            |")
		for _, speedupIJ := range speedup[i] {
			fmt.Printf("%.3f", speedupIJ / nrP)
			fmt.Print("         |")
		}
		fmt.Println()
	}
}
