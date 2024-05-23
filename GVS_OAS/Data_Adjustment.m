clc
close all
clear all

%% Import Data

% Ottieni la lista di tutti i file Excel nella cartella corrente
fileList = dir('*.xls*');

% Inizializza la struttura per contenere tutte le matrici di dati
dataStructure = struct();

% Ciclo per ogni file Excel trovato
for i = 1:length(fileList)
    % Ottieni il nome del file
    filename = fileList(i).name;
    
    % Estrai la data dal nome del file
    dateStr = filename(1:8); % Assumi che i primi 8 caratteri siano la data
    
    % Aggiungi un prefisso alla data per renderla un nome valido del campo
    fieldName = strcat('data_', dateStr);

    % Imposta le opzioni di importazione
    opts = spreadsheetImportOptions("NumVariables", 575);
    opts.Sheet = "Hydrant_Withdrawn";
    opts.DataRange = "A2:VC49";
    opts.VariableNames = ["VarName1", "DERB16", "DERB13", "DERB20", "NODOB3", "DERB8", "NODOL", "NODOM", "NODOH", "NODOB1", "DERB18", "NODOB", "NODOQ", "NODOI", "NODOV", "NODOD", "NODOE", "DERB3", "DERB2", "DERB7", "NODOO", "NODON", "B81", "DERB11", "DER21", "B182", "DER32", "B203", "B455", "DER52", "DER51", "DERB5", "B295", "B305", "DER62", "B916", "B151", "B141", "B131", "DER31", "B213", "DER41", "B334", "B314", "B324", "B23820", "B23920", "B19417", "B19317", "B659", "B669", "B10410", "B10510", "B11012a", "DER12A1", "B14012", "DER122", "DER121", "B14212", "DER161", "B18716", "DER111", "B13311", "B12212a", "B12312a", "B21914", "B29514", "B22114", "DER141", "B12711", "DERB1", "B629", "B639", "DER102", "B10210", "DERB10", "DER101", "B12012a", "DER12A4", "B11112a", "DER12A2", "AM2163", "AM2162", "AM1148", "AM1147", "AH1115", "AH1117", "AI2122", "AI2123", "AF1105", "AF1106", "AF1099", "AF1100", "DERP1", "AP1081", "AP1068", "AP1067", "DERO1", "AO1051", "AF1108", "AF1109", "AS1023", "AS1024", "AC1008", "AC1013", "AR1021", "AR1018", "NODOU", "AU2036", "AO1058", "B10912a", "DERB12a", "B23120", "B23220", "AB1001", "B11", "B21", "B12811", "B14712", "B29612", "DERB4", "AM2157", "NODOM1", "AM2172", "AM2174", "AP1082", "AP1080", "AU3037", "NODOR", "AR1014", "AQ1004", "AQ1003", "DERB19", "B28419", "B28319", "DER201", "B26520", "B24818", "B25018", "B15613", "B15513", "DER142", "B22214", "B18216", "B18116", "DERM1", "AM2182", "NODOZ", "AZ1468", "DERZ1", "AZ1471", "AZ1481", "AV1462", "AV1461", "AI2126", "AI2125", "AH2119", "AH2118", "AH3120", "AN1097", "AN1096", "AN1086", "AN1090", "AN1089", "AN1088", "AL1132", "AL1131", "DERL1", "AL1129", "AM1152", "AM1145", "AM1146", "AM1156", "AM1154", "AF1114", "AF1113", "AF1104", "AF1101", "AF1102", "AE1046", "AO1061", "AO1060", "AO1057", "AO1056", "AO1053", "AO1052", "AD1043", "AD1042", "AD1045", "AD1044", "DERD1", "AD1040", "NODOC", "AC1007", "AQ1005", "NODOS", "AS1022", "NODOT", "DERT1", "AT2029", "AT1029", "AT1028", "AU1035", "AU1034", "DERB17", "B20017", "B19717", "B19817", "AM1135", "AM1134", "AM1137", "AM1138", "DER202", "B26820", "B23520", "B23620", "B27619", "B27519", "B27719", "B27819", "B29119", "B29019", "B24018", "B24118", "B24918", "B25818", "B25718", "DER181", "B25418", "DERB15", "B17015", "B16315", "B16215", "B17115", "DER162", "B18016", "B18316", "B18816", "B18916", "B19116", "B23016", "DER163", "B22816", "B21614", "B21714", "B14913", "B15213", "B15113", "B13712", "B13812", "B12512a", "B12412a", "B12112a", "B11212a", "B896", "DER61", "B866", "B856", "B936", "B926", "B886", "B876", "B52BIS5", "B525", "B495", "B485", "B719", "B709", "B689", "B699", "B619", "B1619", "B1609", "DERB9", "B649", "B608", "B757", "B817", "B827", "B9710", "B9810", "B9910", "B10010", "B91", "B71", "DERB12", "B61", "B51", "B41", "B31", "B111", "B121", "DER22", "B172", "B162", "B223", "B233", "B243", "B253", "B283", "B273", "B193", "B384", "B344", "B354", "B445", "B435", "B425", "B465", "DER53", "B505", "B515", "B475", "DERB6", "B846", "B836", "B906", "B747", "B737", "B727", "B767", "DER72", "B807", "B777", "B787", "B797", "B2977", "B598", "B588", "B578", "B568", "B558", "B548", "B538", "B679", "DER93", "B1599", "B2989", "B1579", "B1589", "B9610", "B9510", "B9410", "B10310", "B10610", "B10710", "B10110", "B10810", "B12911", "B13011", "B13611", "B13511", "B13211", "B13111", "DERB14", "B14612", "B14512", "B14412", "B14312", "B13912", "B14112", "B11312a", "B11412a", "DER12A3", "B11612a", "B11512a", "B11712a", "B11812a", "B11912a", "B15313", "B1", "B15413", "B15013", "B14813", "DERB21", "B22314", "B22414", "B22014", "B21814", "B17215", "B17315", "B17415", "B17515", "B17615", "B17715", "B17815", "DER151", "B16415", "B16615", "B16715", "B16815", "B16915", "B19216", "B22916", "B22516", "B22716", "B22616", "B19016", "B18616", "B17916", "B18416", "B18516", "B19517", "B19617", "B19917", "B28519", "B28619", "B28719", "B28819", "B29219", "B28919", "B28219", "B28119", "B28019", "B27919", "B27419", "B27319", "B27219", "B23720", "B26420", "B26320", "B26220", "B26120", "B26020", "B25920", "B26620", "B26720", "B27020", "B27120", "B23420", "B23320", "AQ1002", "AQ1006", "AC1009", "AC1010", "AC1011", "AC1012", "AR1015", "AR1016", "AR1017", "AR1019", "AR1020", "AS1025", "AS1026", "AT2031", "AT2030", "AT2032", "AT2033", "AT1027", "AD1038", "AD1039", "AD1041", "AE1047", "AE1048", "AO1049", "AO1050", "AO1054", "AO1059", "AO1062", "AO1055", "AP1069", "AP1070", "AP1071", "AP1072", "AP1073", "AP1074", "AP1075", "AP1076", "AP1079", "AP1078", "AN1083", "AN1084", "AN1085", "AN1092", "AN1093", "AN1094", "AN1095", "AN1091", "AN1087", "AF1098", "NODOF", "AF1107", "AF1110", "AF1111", "AF1112", "AF1103", "AH1116", "AI2124", "AV1460", "AV1463", "AV1464", "AV1465", "AV1466", "AV1467", "AZ1480", "AZ1479", "AZ1478", "AZ1477", "AZ1476", "AZ1469", "AZ1470", "AZ1472", "AZ1473", "AZ1474", "AZ1475", "AL1128", "AL1127", "AL1130", "DERM2", "AM1133", "AM1136", "AM1139", "AM1140", "AM1141", "AM1142", "AM1143", "AM1144", "AM1149", "AM1150", "AM1151", "AM1153", "AM2158", "AM2159", "AM2160", "AM2161", "AM2164", "AM2165", "AM2166", "AM2167", "AM2168", "AM2169", "AM2170", "AM2171", "AM2176", "AM2175", "AM2177", "AM2178", "AM2179", "AM2180", "AM2181", "AM2183", "AM2184", "AM2185", "DERB22", "DERA", "B26920", "AP1066", "B102", "B263", "B13411", "B16515", "AP1077", "AP1065", "B24618", "B24518", "B24418", "B24318", "B24218", "B25518", "B25618", "B25318", "B25218", "B25118", "B24718", "B29319", "B29419", "AO1063", "NODOP", "B374", "B364", "B404", "B414", "B394", "AI1121", "VASCA_GRANDE"];
    opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

    % Importa i dati dal file Excel
    data = readmatrix(filename, opts);
    
    % Assegna i dati alla struttura usando la data come nome del campo
    dataStructure.(fieldName) = data;
end


%% Aggiustamento

% Elimino prima colonna di tutte le matrici di dati importati
fields = fieldnames(dataStructure);
for i = 1:numel(fields)
    % Estrai la matrice di dati corrente
    currentMatrix = dataStructure.(fields{i});
    
    % Elimina la prima colonna dalla matrice
    currentMatrix = currentMatrix(:, 2:end);
    
    % Aggiorna la matrice all'interno della struttura dataStructure
    dataStructure.(fields{i}) = currentMatrix;
end

% Creo nuova struttura di dati con tutti i giorni dell'anno
newDataStructure = struct();

% Definisci il numero di giorni per ciascun mese
daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

% Ciclo per ciascun giorno dell'anno
for year = 2007:2007
    for month = 1:12
        % Ottieni il numero di giorni per il mese corrente
        numDays = daysInMonth(month);
        
        % Ciclo per ciascun giorno del mese
        for day = 1:numDays
            % Crea il nome del campo
            dateStr = sprintf('%04d%02d%02d', year, month, day);
            fieldName = strcat('data_', dateStr);
            
            % Crea una matrice di zeri 48x574
            dataMatrix = zeros(48, 574);
            
            % Assegna la matrice al campo nella nuova struct
            newDataStructure.(fieldName) = dataMatrix;
        end
    end
end

% Inserisco dati importati nella matrice dell'anno

fields = fieldnames(dataStructure);
for i = 1:numel(fields)
    % Estrai il nome del campo corrente
    fieldName = fields{i};
    
    % Verifica se il campo corrispondente esiste in NewDataStructure
    matchingField = find(strcmp(fieldnames(newDataStructure), fieldName));
    if ~isempty(matchingField)
        % Se esiste, sostituisci la matrice di zeri con i dati dalla struttura DataStructure
        newDataStructure.(fieldName) = dataStructure.(fieldName);
    end
end

% Creo matrice unica
concatenatedMatrix = [];

% Ciclo per ciascun campo della struttura newDataStructure
fields = fieldnames(newDataStructure);
for i = 1:numel(fields)
    % Estrai la matrice di dati corrente e trasponila
    currentMatrix = newDataStructure.(fields{i});
    currentMatrixTransposed = currentMatrix.';
    
    % Aggiungi la matrice trasposta alla matrice concatenata
    concatenatedMatrix = [concatenatedMatrix, currentMatrixTransposed];
end

%% Salvataggio nuovo file txt

% Definisci il nome del file di output
outputFileName = '2007_Hydrant_Withdrawn.txt';

% Salva la matrice come file di testo
outputFilePath = fullfile(pwd, outputFileName);
writematrix(concatenatedMatrix, outputFilePath, 'Delimiter', ' ');
