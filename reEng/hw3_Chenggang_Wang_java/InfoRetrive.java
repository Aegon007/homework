import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class InfoRetrive {
    public static void main(String[] args) {
        Computing.OutPut();
    }
}

class Computing {
    public static void OutPut() {
        System.out.println("Hello world!");
    }

    private static double computeSimilarity(){
        double rtn = 0.00;
        return rtn;
    }

    private static double computeTermFrequency() {
        double rtn = 0.00;
        return rtn;
    }

    private static double computeInverseDocFrequency() {
        double rtn = 0.00;
        return rtn;
    }
}

class TextDataProcessor {
    public static List<String> getTermList() {
        List<String> rtnList = new ArrayList<String>();
        return rtnList;
    }

    public static Map<String, List> readFile(String fpath) {
        Map<String, List> rtnDict = new Map<String, List>();
        List<String> frList = new ArrayList<String>();
        List<String> nfrList = new ArrayList<String>();

        try {
            File file = new File(fpath);
            if (file.isFile() && file.exists()){
                InputStreamReader read = new InputStreamReader(new FileInputStream(file));
                BufferedReader bufferedReader = new BufferedReader(read);
                String lineTxt = null;

                while ((lineTxt=bufferedReader.readLine())!=null) {
                    frList.add(lineTxt);
                }
                bufferedReader.close();
                read.close();
            } else {
                System.out.println("can not find the file");
            }
        } catch (Exception e) {
            System.out.println("error happened when reading the file");
            e.printStackTrace();
        }

        rtnDict.put("FR", frList);
        rtnDict.put("NFR", nfrList);
        return rtnDict;
    }
}

