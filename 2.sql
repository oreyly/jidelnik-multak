DECLARE VARIABLE DD DATE;
DECLARE VARIABLE D_OBJEDNAVANI_  TIMESTAMP ; --CURRENT_TIME  -- čas objednáváni
BEGIN
  D_OBJEDNAVANI_ =  'NOW';
  DD = D_OD_;
  WHILE (DD<= D_DO_) DO
  BEGIN


    FOR SELECT JIDELAK_NR, DATUM, LFD_NN, SKLD_NR, SKLAD_NR ,CENA , CENADPH, SKLD_NAZEV, ALG_CISLA_0, ALG_NAZEV_0,OBJEDNAVKA0, T_CAS0,POCET ,MOZNOST_OBJEDNAVAT, MOZNOST_BURZA  ,MOZNOST_BURZA_VLOZIT ,JE_VBURZE ,MAM_VBURZE ,MAX_POCET_OBJ_JIDEL, SKLD_CENADPH 
    FROM JIDELNA_JIDELAK_VYPIS_DW(:DD,:LFD_JAZYK_,:LFD_JI_TYP_, :LFD_JI_TYP_CAST_, :LFD_JIDELNA_,:ZA_NR_, :D_OBJEDNAVANI_) 
    ORDER BY DATUM, LFD_NN
    INTO  :JIDELAK_NR, :DATUM, :LFD_NN, :SKLD_NR, :SKLAD_NR ,:CENA , :CENADPH, :SKLD_NAZEV,  :ALG_CISLA_0, :ALG_NAZEV_0 ,:OBJEDNAVKA0, :T_CAS0,:POCET , :MOZNOST_OBJEDNAVAT, :MOZNOST_BURZA  ,:MOZNOST_BURZA_VLOZIT ,:JE_VBURZE ,:MAM_VBURZE ,:MAX_POCET_OBJ_JIDEL,:SKLD_CENADPH
    DO 
    BEGIN 
      SUSPEND;
    END
    DD = DD + 1;
  END
END