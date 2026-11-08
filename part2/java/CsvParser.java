package part2.java;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class CsvParser {

    static final int MAX_ROWS = 20;

    public static void main(String[] args) {
        String fileName = args.length > 0 ? args[0] : "data.csv";

        List<String> lines = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.isBlank()) {
                    lines.add(line);
                }
            }
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
            return;
        }

        if (lines.isEmpty()) {
            System.out.println("File is empty");
            return;
        }

        String firstLine = lines.get(0);
        if (firstLine.startsWith("\uFEFF")) {
            lines.set(0, firstLine.substring(1));
        }

        String delimiter = detectDelimiter(lines.get(0));

        String[] header = lines.get(0).split(delimiter, -1);
        List<String[]> rows = new ArrayList<>();
        for (int i = 1; i < lines.size(); i++) {
            rows.add(lines.get(i).split(delimiter, -1));
        }

        System.out.println("File:      " + fileName);
        System.out.println("Delimiter: " + describe(delimiter));
        System.out.println("Columns:   " + header.length);
        System.out.println("Rows:      " + rows.size());
        System.out.println();

        printTable(header, rows);
    }

    // helpers

    static String detectDelimiter(String headerLine) {
        String[] candidates = { ",", ";", "\t" };
        String best = ",";
        int bestCount = 0;

        for (String c : candidates) {
            int count = headerLine.length() - headerLine.replace(c, "").length();
            if (count > bestCount) {
                best = c;
                bestCount = count;
            }
        }
        return best;
    }

    static String describe(String delimiter) {
        return switch (delimiter) {
            case "," -> "comma (,)";
            case ";" -> "semicolon (;)";
            case "\t" -> "tab";
            default -> delimiter;
        };
    }

    static void printTable(String[] header, List<String[]> rows) {
        int shown = Math.min(rows.size(), MAX_ROWS);

        int[] widths = new int[header.length];
        for (int j = 0; j < header.length; j++) {
            widths[j] = header[j].length();
        }
        for (int i = 0; i < shown; i++) {
            String[] row = rows.get(i);
            for (int j = 0; j < header.length && j < row.length; j++) {
                widths[j] = Math.max(widths[j], row[j].length());
            }
        }

        printRow(header, widths);

        StringBuilder separator = new StringBuilder();
        for (int j = 0; j < widths.length; j++) {
            if (j > 0)
                separator.append("-+-");
            separator.append("-".repeat(widths[j]));
        }
        System.out.println(separator);

        for (int i = 0; i < shown; i++) {
            printRow(rows.get(i), widths);
        }

        if (rows.size() > shown) {
            System.out.println("... and " + (rows.size() - shown) + " more rows");
        }
    }

    static void printRow(String[] values, int[] widths) {
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < widths.length; j++) {
            String value = j < values.length ? values[j] : "";
            if (j > 0)
                sb.append(" | ");
            sb.append(String.format("%-" + widths[j] + "s", value));
        }
        System.out.println(sb);
    }
}
