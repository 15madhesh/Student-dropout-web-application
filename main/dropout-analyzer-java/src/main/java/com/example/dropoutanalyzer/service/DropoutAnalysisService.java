package com.example.dropoutanalyzer.service;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

@Service
public class DropoutAnalysisService {

    public Map<String, Object> analyzeManualEntry(Map<String, String> data) {
        Map<String, Object> result = new HashMap<>();
        result.put("stud_name", data.get("stud_name"));
        result.put("dob", data.get("dob"));
        result.put("status", data.get("status"));
        result.put("sslc_marks", data.get("sslc_marks"));
        result.put("hsc_marks", data.get("hsc_marks"));
        result.put("clg_name", data.get("clg_name"));
        result.put("mother_name", data.get("mother_name"));
        result.put("father_name", data.get("father_name"));
        result.put("address", data.get("address"));

        try {
            double sslc = Double.parseDouble(data.getOrDefault("sslc_marks", "0"));
            double hsc = Double.parseDouble(data.getOrDefault("hsc_marks", "0"));
            double dropoutRate = (1 - (sslc / 100)) * (1 - (hsc / 100));
            result.put("dropout_rate", dropoutRate);
        } catch (NumberFormatException e) {
            result.put("dropout_rate", null);
        }
        return result;
    }

    public List<Map<String, Object>> analyzeCSV(Path csvFilePath) throws IOException {
        List<Map<String, Object>> results = new ArrayList<>();

        try (Reader reader = Files.newBufferedReader(csvFilePath);
             CSVParser csvParser = new CSVParser(reader, CSVFormat.DEFAULT.withFirstRecordAsHeader())) {

            for (CSVRecord record : csvParser) {
                try {
                    String name = record.get("name");
                    double age = Double.parseDouble(record.get("age"));
                    double attendance = Double.parseDouble(record.get("attendance"));
                    double marks = Double.parseDouble(record.get("marks"));
                    double dropoutRate = (1 - (attendance / 100)) * (1 - (marks / 100));

                    Map<String, Object> studentData = new HashMap<>();
                    studentData.put("name", name);
                    studentData.put("age", age);
                    studentData.put("attendance", attendance);
                    studentData.put("marks", marks);
                    studentData.put("dropout_rate", dropoutRate);

                    results.add(studentData);
                } catch (Exception e) {
                    // Skip invalid records
                }
            }
        }

        if (results.isEmpty()) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Invalid CSV format. Ensure columns: name,age,attendance,marks");
            error.put("students", new ArrayList<>());
            results.add(error);
        }

        return results;
    }

    public double calculateDropoutPercentage(List<Map<String, Double>> marksList, double attendancePercent) {
        List<Double> internalMarks = new ArrayList<>();
        List<Double> cgpas = new ArrayList<>();

        for (Map<String, Double> mark : marksList) {
            for (Map.Entry<String, Double> entry : mark.entrySet()) {
                String key = entry.getKey();
                Double value = entry.getValue();
                if (key.startsWith("internal") && value != null) {
                    internalMarks.add(value);
                }
                if ("cgpa".equals(key) && value != null) {
                    cgpas.add(value);
                }
            }
        }

        double avgInternal = internalMarks.stream().mapToDouble(Double::doubleValue).average().orElse(0);
        double avgCgpa = cgpas.stream().mapToDouble(Double::doubleValue).average().orElse(0);

        double dropoutPercentage = ((1 - (avgInternal / 100)) * 0.3 +
                (1 - (avgCgpa / 10)) * 0.5 +
                (1 - (attendancePercent / 100)) * 0.2) * 100;

        dropoutPercentage = Math.max(0, Math.min(dropoutPercentage, 100));

        return Math.round(dropoutPercentage * 100.0) / 100.0;
    }
}
