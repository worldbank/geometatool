# -*- coding: utf-8 -*-
# A substantial portion of this code was adapted from the repository at "https://github.com/AlexZeller/ISO19115-3Creator."

import logging
import xml.etree.ElementTree as ET 
from xml.dom import minidom 

#Set up logging
log = logging.getLogger(__name__)

# Namespaces
xsi ='http://www.w3.org/2001/XMLSchema-instance'
xlink = 'http://www.w3.org/1999/xlink'
gml = 'http://www.opengis.net/gml/3.2'
cat = 'http://standards.iso.org/iso/19115/-3/cat/1.0'
gco = 'http://standards.iso.org/iso/19115/-3/gco/1.0'
gcx = 'http://standards.iso.org/iso/19115/-3/gcx/1.0'
gex = 'http://standards.iso.org/iso/19115/-3/gex/1.0'
lan = 'http://standards.iso.org/iso/19115/-3/lan/1.0'
mas = 'http://standards.iso.org/iso/19115/-3/mas/1.0'
mcc = 'http://standards.iso.org/iso/19115/-3/mcc/1.0'
mco = 'http://standards.iso.org/iso/19115/-3/mco/1.0'
mda = 'http://standards.iso.org/iso/19115/-3/mda/1.0'
mdq = 'http://standards.iso.org/iso/19157/-2/mdq/1.0'
mex = 'http://standards.iso.org/iso/19115/-3/mex/1.0'
mmi = 'http://standards.iso.org/iso/19115/-3/mmi/1.0'
mpc = 'http://standards.iso.org/iso/19115/-3/mpc/1.0'
mrd = 'http://standards.iso.org/iso/19115/-3/mrd/1.0'
mri = 'http://standards.iso.org/iso/19115/-3/mri/1.0'
mrs = 'http://standards.iso.org/iso/19115/-3/mrs/1.0'
cit = 'http://standards.iso.org/iso/19115/-3/cit/2.0'
mac = 'http://standards.iso.org/iso/19115/-3/mac/2.0'
mdb = 'http://standards.iso.org/iso/19115/-3/mdb/2.0'
mds = 'http://standards.iso.org/iso/19115/-3/mds/2.0'
mdt = 'http://standards.iso.org/iso/19115/-3/mdt/2.0'
mrl = 'http://standards.iso.org/iso/19115/-3/mrl/2.0'
mrc = 'http://standards.iso.org/iso/19115/-3/mrc/2.0'
msr = 'http://standards.iso.org/iso/19115/-3/msr/2.0'
srv = 'http://standards.iso.org/iso/19115/-3/srv/2.0'
fcc = 'http://standards.iso.org/iso/19110/fcc/1.0'
gfc = 'http://standards.iso.org/iso/19110/gfc/1.1'

ET.register_namespace('xsi',xsi)
ET.register_namespace('xlink',xlink)
ET.register_namespace('gml',gml)
ET.register_namespace('cat',cat)
ET.register_namespace('gco',gco)
ET.register_namespace('gcx',gcx)
ET.register_namespace('gex',gex)
ET.register_namespace('lan',lan)
ET.register_namespace('mas',mas)
ET.register_namespace('mcc',mcc)
ET.register_namespace('mco',mco)
ET.register_namespace('mda',mda)
ET.register_namespace('mdq',mdq)
ET.register_namespace('mex',mex)
ET.register_namespace('mmi',mmi)
ET.register_namespace('mpc',mpc)
ET.register_namespace('mrd',mrd)
ET.register_namespace('mri',mri)
ET.register_namespace('mrs',mrs)
ET.register_namespace('cit',cit)
ET.register_namespace('mac',mac)
ET.register_namespace('mdb',mdb)
ET.register_namespace('mds',mds)
ET.register_namespace('mdt',mdt)
ET.register_namespace('mrl',mrl)
ET.register_namespace('mrc',mrc)
ET.register_namespace('msr',msr)
ET.register_namespace('srv',srv)
ET.register_namespace('fcc',fcc)
ET.register_namespace('gfc',gfc)

#CodeLists
codelist_LanguageCode = 'http://standards.iso.org/19115/-3/lan/1.0/codelists.xml#LanguageCode'
codelist_MD_CharacterSetCode = 'http://standards.iso.org/19115/-3/lan/1.0/codelists.xml#MD_CharacterSetCode'
codelist_MD_ScopeCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_ScopeCode'
codelist_CI_RoleCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_RoleCode'
codelist_CI_DateTypeCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode'
codelist_MD_ReferenceSystemTypeCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_ReferenceSystemTypeCode'
codelist_MD_ProgressCode = 'http://standards.iso.org/iso/19115/resources/Codelist/cat/codelists.xml#MD_ProgressCode'
codelist_MD_ClassificationCode = 'http://standards.iso.org/iso/19115/resources/Codelist/cat/codelists.xml#MD_ClassificationCode'
codelist_MD_TopologyLevelCode = 'http://standards.iso.org/iso/19115/resources/Codelist/cat/codelists.xml#MD_TopologyLevelCode'
codelist_MD_GeometricObjectTypeCode = 'http://standards.iso.org/iso/19115/resources/Codelist/cat/codelists.xml#MD_GeometricObjectTypeCode'
codelist_DS_AssociationTypeCode = 'http://standards.iso.org/iso/19115/resources/Codelist/cat/codelists.xml#DS_AssociationTypeCode'
codelist_MD_CoverageContentTypeCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_CoverageContentTypeCode'
codelist_MD_CellGeometryCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_CellGeometryCode'
codelist_MD_DimensionNameTypeCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_DimensionNameTypeCode'

class ISO_Metadata:
    '''Class to create ISO19115-3 Metadata Entries.'''
    
    def __init__(self):
        # self.root = ET.Element('{'+ mdb +'}MD_Metadata', attrib={"{" + xsi + "}schemaLocation" : schemaLocation})
        self.root = ET.Element('{'+ mdb +'}MD_Metadata')
         
          
    def prettify(self):
        '''Return a pretty-printed XML string for the Element.'''
        rough_string = ET.tostring(self.root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    

    def save_to_file(self, file_path):
        xml_metadata = self.prettify()
        output_file = open(file_path, 'w' )
        output_file.write(xml_metadata)
        output_file.close()
    

    def metadataIdentifier(self, UUID):
        a = ET.SubElement(self.root, '{'+ mdb +'}metadataIdentifier')
        b = ET.SubElement(a, '{'+ mcc +'}MD_Identifier')
        c = ET.SubElement(b, '{'+ mcc +'}code')
        d = ET.SubElement(c, '{'+ gco +'}CharacterString')
        d.text = UUID
        

    def defaultLocale(self, languageCode, characterSetCode):
        a = ET.SubElement(self.root, '{'+ mdb +'}defaultLocale')
        b = ET.SubElement(a, '{'+ lan +'}PT_Locale')
        c = ET.SubElement(b, '{'+ lan +'}language')
        ET.SubElement(c, '{'+ lan +'}LanguageCode', codeList=codelist_LanguageCode, codeListValue=languageCode)
        
        d = ET.SubElement(b, '{'+ lan +'}characterEncoding')
        ET.SubElement(d, '{'+ lan +'}MD_CharacterSetCode', codeList=codelist_MD_CharacterSetCode, codeListValue=characterSetCode)


    def metadataScope(self, scopeCode):
        a = ET.SubElement(self.root, '{'+ mdb +'}metadataScope')
        b = ET.SubElement(a, '{'+ mdb +'}MD_MetadataScope')
        c = ET.SubElement(b, '{'+ mdb +'}resourceScope')
        ET.SubElement(c, '{'+ mcc +'}MD_ScopeCode', codeList=codelist_MD_ScopeCode, codeListValue=scopeCode)
        

    def contact(self, organisationName, individualName, roleCode):
        a = ET.SubElement(self.root, '{'+ mdb +'}contact')
        b = ET.SubElement(a, '{'+ cit +'}CI_Responsibility')
        c = ET.SubElement(b, '{'+ cit +'}role')
        ET.SubElement(c, '{'+ cit +'}CI_RoleCode', codeList=codelist_CI_RoleCode, codeListValue=roleCode)    

        g = ET.SubElement(b, '{'+ cit +'}party')
        d = ET.SubElement(g, '{'+ cit +'}CI_Organisation')
        e = ET.SubElement(d, '{'+ cit +'}name')
        f = ET.SubElement(e, '{'+ gco +'}CharacterString')
        f.text = organisationName

        if individualName:
            h = ET.SubElement(d, '{'+ cit +'}individual')
            i = ET.SubElement(h, '{'+ cit +'}CI_Individual')
            j = ET.SubElement(i, '{'+ cit +'}name')
            k = ET.SubElement(j, '{'+ gco +'}CharacterString')
            k.text = individualName
        

    def dateInfo(self, dateTime, dateTypeCode):
        a = ET.SubElement(self.root, '{'+ mdb +'}dateInfo')
        b = ET.SubElement(a, '{'+ cit +'}CI_Date')
        c = ET.SubElement(b, '{'+ cit +'}date')
        d = ET.SubElement(c, '{'+ gco +'}Date')
        d.text = dateTime       
        e = ET.SubElement(b, '{'+ cit +'}dateType')
        ET.SubElement(e, '{'+ cit +'}CI_DateTypeCode', codeList=codelist_CI_DateTypeCode, codeListValue=dateTypeCode)
        

    def referenceSystemInfo(self, EPSG_Code, referenceSystemTypeCode):
        a = ET.SubElement(self.root, '{'+ mdb +'}referenceSystemInfo')
        b = ET.SubElement(a, '{'+ mrs +'}MD_ReferenceSystem')
        c = ET.SubElement(b, '{'+ mrs +'}referenceSystemIdentifier')
        d = ET.SubElement(c, '{'+ mcc +'}MD_Identifier')
        e = ET.SubElement(d, '{'+ mcc +'}code')
        f = ET.SubElement(e, '{'+ gco +'}CharacterString')
        f.text = EPSG_Code
        
        g = ET.SubElement(d, '{'+ mcc +'}codeSpace')
        h = ET.SubElement(g, '{'+ gco +'}CharacterString')
        h.text = 'EPSG'      
        i = ET.SubElement(b, '{'+ mrs +'}referenceSystemType')
        ET.SubElement(i, '{'+ mrs +'}MD_ReferenceSystemTypeCode', codeList=codelist_MD_ReferenceSystemTypeCode, codeListValue=referenceSystemTypeCode)


    def identificationInfo(self, datasetTitle, abstract, progressCode, spatialResolution, BBOX, timePeriod, formatTitle, keywords, classificationCode, useLimitation):
        a = ET.SubElement(self.root, '{'+ mdb +'}identificationInfo')
        b = ET.SubElement(a, '{'+ mri +'}MD_DataIdentification')
        
        c = ET.SubElement(b, '{'+ mri +'}citation')
        d = ET.SubElement(c, '{'+ cit +'}CI_Citation')
        e = ET.SubElement(d, '{'+ cit +'}title')
        f = ET.SubElement(e, '{'+ gco +'}CharacterString')
        f.text = datasetTitle
        
        k = ET.SubElement(b, '{'+ mri +'}abstract')
        l = ET.SubElement(k, '{'+ gco +'}CharacterString')
        l.text = abstract
        
        m = ET.SubElement(b, '{'+ mri +'}status')
        ET.SubElement(m, '{'+ mcc +'}MD_ProgressCode', codeList=codelist_MD_ProgressCode, codeListValue=progressCode)

        if spatialResolution:
            ar = ET.SubElement(b, '{'+ mri +'}spatialResolution')
            at = ET.SubElement(ar, '{'+ mri +'}MD_Resolution')
            au = ET.SubElement(at, '{'+ mri +'}distance')
            av = ET.SubElement(au, '{'+ gco +'}Distance', uom="meter")
            av.text = str(spatialResolution)

        n = ET.SubElement(b, '{'+ mri +'}extent')
        o = ET.SubElement(n, '{'+ gex +'}EX_Extent')
        
        p = ET.SubElement(o, '{'+ gex +'}geographicElement')
        q = ET.SubElement(p, '{'+ gex +'}EX_GeographicBoundingBox')
        r = ET.SubElement(q, '{'+ gex +'}westBoundLongitude')
        s = ET.SubElement(r, '{'+ gco +'}Decimal')
        s.text = BBOX[0]
        t = ET.SubElement(q, '{'+ gex +'}eastBoundLongitude')
        u = ET.SubElement(t, '{'+ gco +'}Decimal')
        u.text = BBOX[2]
        v = ET.SubElement(q, '{'+ gex +'}southBoundLatitude')
        w = ET.SubElement(v, '{'+ gco +'}Decimal')
        w.text = BBOX[1]
        x = ET.SubElement(q, '{'+ gex +'}northBoundLatitude')
        y = ET.SubElement(x, '{'+ gco +'}Decimal')
        y.text = BBOX[3]
        
        al = ET.SubElement(o, '{'+ gex +'}temporalElement')
        am = ET.SubElement(al, '{'+ gex +'}EX_TemporalExtent')
        an = ET.SubElement(am, '{'+ gex +'}extent')
        ao = ET.SubElement(an, '{'+ gml +'}TimePeriod')
        ao.set('gml:id','TimePeriod')
        ap = ET.SubElement(ao, '{'+ gml +'}beginPosition')
        aq = ET.SubElement(ao, '{'+ gml +'}endPosition')
        ap.text = timePeriod[0]
        aq.text = timePeriod[1]
        
        z = ET.SubElement(b, '{'+ mri +'}resourceFormat')
        aa = ET.SubElement(z, '{'+ mrd +'}MD_Format')
        ab = ET.SubElement(aa, '{'+ mrd +'}formatSpecificationCitation')
        ac = ET.SubElement(ab, '{'+ cit +'}CI_Citation')
        ad = ET.SubElement(ac, '{'+ cit +'}title')
        af = ET.SubElement(ad, '{'+ gco +'}CharacterString')
        af.text = formatTitle
        
        if keywords:
            ag = ET.SubElement(b, '{'+ mri +'}descriptiveKeywords')
            ah = ET.SubElement(ag, '{'+ mri +'}MD_Keywords')
            
            for Keyword in keywords:          
                aj = ET.SubElement(ah, '{'+ mri +'}keyword')
                ak = ET.SubElement(aj, '{'+ gco +'}CharacterString')
                ak.text = Keyword  
            
        ba = ET.SubElement(b, '{'+ mri +'}resourceConstraints')
        bb = ET.SubElement(ba, '{'+ mco +'}MD_SecurityConstraints')
        
        bc = ET.SubElement(bb, '{'+ mco +'}classification')
        ET.SubElement(bc, '{'+ mco +'}MD_ClassificationCode', codeList=codelist_MD_ClassificationCode, codeListValue=classificationCode)
        
        be = ET.SubElement(bb, '{'+ mco +'}userNote')
        bf = ET.SubElement(be, '{'+ gco +'}CharacterString')
        bf.text = useLimitation        

#        bg = ET.SubElement(b, '{'+ mri +'}associatedResource')
#        bh = ET.SubElement(bg, '{'+ mri +'}MD_AssociatedResource')
#        bi = ET.SubElement(bh, '{'+ mri +'}associationType') 
#        ET.SubElement(bi, '{'+ mri +'}DS_AssociationTypeCode', codeList=codelist_DS_AssociationTypeCode, codeListValue='largerWorkCitation')    
#        bk = ET.SubElement(bh, '{'+ mri +'}metadataReference')
#        bl = ET.SubElement(bk, '{'+ cit +'}CI_Citation')
#        bm = ET.SubElement(bl, '{'+ cit +'}title')
#        bn = ET.SubElement(bm, '{'+ gco +'}CharacterString')
#        bn.text = AssociatedResource[0]
#        bo = ET.SubElement(bl, '{'+ cit +'}identifier')
#        bp = ET.SubElement(bo, '{'+ mcc +'}MD_Identifier')
#        bq = ET.SubElement(bp, '{'+ mcc +'}code')
#        br = ET.SubElement(bq, '{'+ gco +'}CharacterString')
#        br.text = AssociatedResource[1] 


    def distributionInfo(self, description, mediumName):
        a = ET.SubElement(self.root, '{'+ mdb +'}distributionInfo')
        b = ET.SubElement(a, '{'+ mrd +'}MD_Distribution')
        
        c = ET.SubElement(b, '{'+ mrd +'}description')
        d = ET.SubElement(c, '{'+ gco +'}CharacterString')
        d.text = description
        
        c = ET.SubElement(b, '{'+ mrd +'}transferOptions')
        d = ET.SubElement(c, '{'+ mrd +'}MD_DigitalTransferOptions')
        e = ET.SubElement(d, '{'+ mrd +'}offLine')
        f = ET.SubElement(e, '{'+ mrd +'}MD_Medium')
        g = ET.SubElement(f, '{'+ mrd +'}name')
        h = ET.SubElement(g, '{'+ cit +'}CI_Citation')
        i = ET.SubElement(h, '{'+ cit +'}title')
        j = ET.SubElement(i, '{'+ gco +'}CharacterString')
        j.text = mediumName
        

    def acquisitionInformation(self, scopeCode, platformCode, platformDescription, instrumentCode, instrumentDescription):
        a = ET.SubElement(self.root, '{'+ mdb +'}acquisitionInformation')
        b = ET.SubElement(a, '{'+ mac +'}MI_AcquisitionInformation') 
        
        c = ET.SubElement(b, '{'+ mac +'}scope')
        t = ET.SubElement(c, '{'+ mcc +'}MD_Scope')
        u = ET.SubElement(t, '{'+ mcc +'}level')
        ET.SubElement(u, '{'+ mcc +'}MD_ScopeCode', codeList=codelist_MD_ScopeCode, codeListValue=scopeCode)

        d = ET.SubElement(b, '{'+ mac +'}platform')
        e = ET.SubElement(d, '{'+ mac +'}MI_Platform')
        
        f = ET.SubElement(e, '{'+ mac +'}identifier')
        
        g = ET.SubElement(f, '{'+ mcc +'}MD_Identifier')
        h = ET.SubElement(g, '{'+ mcc +'}code')
        i = ET.SubElement(h, '{'+ gco +'}CharacterString')
        i.text = platformCode
        
        j = ET.SubElement(e, '{'+ mac +'}description')
        k = ET.SubElement(j, '{'+ gco +'}CharacterString')
        k.text = platformDescription
        
        l = ET.SubElement(e, '{'+ mac +'}instrument')
        m = ET.SubElement(l, '{'+ mac +'}MI_Instrument')
        n = ET.SubElement(m, '{'+ mac +'}identifier')
        o = ET.SubElement(n, '{'+ mcc +'}MD_Identifier')
        p = ET.SubElement(o, '{'+ mcc +'}code')
        q = ET.SubElement(p, '{'+ gco +'}CharacterString')
        q.text = instrumentCode
        r = ET.SubElement(m, '{'+ mac +'}type')
        s = ET.SubElement(r, '{'+ gco +'}CharacterString')
        s.text = instrumentDescription


    def spatialRepresentationInfo(self, vectorSpatialRepresentation=None, gridSpatialRepresentation=None):
        a = ET.SubElement(self.root, '{'+ mdb +'}spatialRepresentationInfo')
        if vectorSpatialRepresentation:
            b = ET.SubElement(a, '{'+ msr +'}MD_VectorSpatialRepresentation')
            c = ET.SubElement(b, '{'+ msr +'}topologyLevel')
            ET.SubElement(c, '{'+ msr +'}MD_TopologyLevelCode', codeList=codelist_MD_TopologyLevelCode, codeListValue=vectorSpatialRepresentation['topologyLevelCode'])
            
            for geometricObjects in vectorSpatialRepresentation['geometricObjectsList']:
                d = ET.SubElement(b, '{'+ msr +'}geometricObjects')
                e = ET.SubElement(d, '{'+ msr +'}MD_GeometricObjects')
                f = ET.SubElement(e, '{'+ msr +'}geometricObjectType')
                ET.SubElement(f, '{'+ msr +'}MD_GeometricObjectTypeCode', codeList=codelist_MD_GeometricObjectTypeCode, codeListValue=geometricObjects['objectType'])
                g = ET.SubElement(e, '{'+ msr +'}geometricObjectCount')
                h = ET.SubElement(g, '{'+ gco +'}Integer')
                h.text = str(geometricObjects['count'])

        if gridSpatialRepresentation:
            b = ET.SubElement(a, '{'+ msr +'}MD_GridSpatialRepresentation')
            c = ET.SubElement(b, '{'+ msr +'}numberOfDimensions')
            d = ET.SubElement(c, '{'+ gco +'}Integer')
            d.text = str(gridSpatialRepresentation['numberOfDimensions'])

            e = ET.SubElement(b, '{'+ msr +'}axisDimensionProperties')
            f = ET.SubElement(e, '{'+ msr +'}MD_Dimension')
            g = ET.SubElement(f, '{'+ msr +'}dimensionName')
            ET.SubElement(g, '{'+ msr +'}MD_DimensionNameTypeCode', codeList=codelist_MD_DimensionNameTypeCode, codeListValue="row")
            g = ET.SubElement(f, '{'+ msr +'}dimensionSize')
            h = ET.SubElement(g, '{'+ gco +'}Integer')
            h.text = str(gridSpatialRepresentation['rowSize'])
            i = ET.SubElement(f, '{'+ msr +'}resolution')
            j = ET.SubElement(i, '{'+ gco +'}Distance', uom=gridSpatialRepresentation['resolutionUnit'])
            j.text = str(gridSpatialRepresentation['rowResolution'])

            e = ET.SubElement(b, '{'+ msr +'}axisDimensionProperties')
            f = ET.SubElement(e, '{'+ msr +'}MD_Dimension')
            g = ET.SubElement(f, '{'+ msr +'}dimensionName')
            ET.SubElement(g, '{'+ msr +'}MD_DimensionNameTypeCode', codeList=codelist_MD_DimensionNameTypeCode, codeListValue="column")
            g = ET.SubElement(f, '{'+ msr +'}dimensionSize')
            h = ET.SubElement(g, '{'+ gco +'}Integer')
            h.text = str(gridSpatialRepresentation['columnSize'])
            i = ET.SubElement(f, '{'+ msr +'}resolution')
            j = ET.SubElement(i, '{'+ gco +'}Distance', uom=gridSpatialRepresentation['resolutionUnit'])
            j.text = str(gridSpatialRepresentation['columnResolution'])

            e = ET.SubElement(b, '{'+ msr +'}cellGeometry')
            ET.SubElement(e, '{'+ msr +'}MD_CellGeometryCode', codeList=codelist_MD_CellGeometryCode, codeListValue=gridSpatialRepresentation['cellGeometryCode'])

            f = ET.SubElement(b, '{'+ msr +'}transformationParameterAvailability')
            g = ET.SubElement(f, '{'+ gco +'}Boolean')
            g.text = gridSpatialRepresentation['transformationParameterAvailability']

    
    def featureCatalogue(self, featureCatalogueName, featureCatalogueScopes, versionNumber, versionDate, languageCode, organisationName, individualName, roleCode, featureTypeList):
        a = ET.SubElement(self.root, '{'+ mdb +'}contentInfo')
        b = ET.SubElement(a, '{'+ mrc +'}MD_FeatureCatalogue')
        c = ET.SubElement(b, '{'+ mrc +'}featureCatalogue') 
        d = ET.SubElement(c, '{'+ gfc +'}FC_FeatureCatalogue') 
        e = ET.SubElement(d, '{'+ cat +'}name')
        f = ET.SubElement(e, '{'+ gco +'}CharacterString')
        f.text = featureCatalogueName

        for scope in featureCatalogueScopes:
            e = ET.SubElement(d, '{'+ cat +'}scope')
            f = ET.SubElement(e, '{'+ gco +'}CharacterString')
            f.text = scope

        e = ET.SubElement(d, '{'+ cat +'}versionNumber')
        f = ET.SubElement(e, '{'+ gco +'}CharacterString')
        f.text = versionNumber

        e = ET.SubElement(d, '{'+ cat +'}versionDate')
        f = ET.SubElement(e, '{'+ gco +'}Date')
        f.text = versionDate

        e = ET.SubElement(d, '{'+ cat +'}language')
        ET.SubElement(e, '{'+ lan +'}LanguageCode', codeList=codelist_LanguageCode, codeListValue=languageCode)

        e = ET.SubElement(d, '{'+ gfc +'}producer')
        f = ET.SubElement(e, '{'+ cit +'}CI_Responsibility')
        g = ET.SubElement(f, '{'+ cit +'}role')
        ET.SubElement(g, '{'+ cit +'}CI_RoleCode', codeList=codelist_CI_RoleCode, codeListValue=roleCode)    
        g = ET.SubElement(f, '{'+ cit +'}party')
        h = ET.SubElement(g, '{'+ cit +'}CI_Organisation')
        i = ET.SubElement(h, '{'+ cit +'}name')
        j = ET.SubElement(i, '{'+ gco +'}CharacterString')
        j.text = organisationName
        i = ET.SubElement(h, '{'+ cit +'}individual')
        j = ET.SubElement(i, '{'+ cit +'}CI_Individual')
        k = ET.SubElement(j, '{'+ cit +'}name')
        l = ET.SubElement(k, '{'+ gco +'}CharacterString')
        l.text = individualName

        for featureType in featureTypeList:
            f = ET.SubElement(d, '{'+ gfc +'}featureType')
            g = ET.SubElement(f, '{'+ gfc +'}FC_FeatureType')
            h = ET.SubElement(g, '{'+ gfc +'}typeName')
            h.text = featureType['typeName']

            i = ET.SubElement(g, '{'+ gfc +'}definition')
            j = ET.SubElement(i, '{'+ gco +'}CharacterString')
            j.text = featureType['definition']

            k = ET.SubElement(g, '{'+ gfc +'}isAbstract')
            l = ET.SubElement(k, '{'+ gco +'}Boolean')
            l.text = 'false'

            for carrierOfCharacteristics in featureType['carrierOfCharacteristicsList']:
                m = ET.SubElement(g, '{'+ gfc +'}carrierOfCharacteristics')
                n = ET.SubElement(m, '{'+ gfc +'}FC_FeatureAttribute')
                o = ET.SubElement(n, '{'+ gfc +'}memberName')
                o.text = carrierOfCharacteristics['memberName']

                o = ET.SubElement(n, '{'+ gfc +'}cardinality')
                p = ET.SubElement(o, '{'+ gco +'}CharacterString')
                p.text = '1'

                q = ET.SubElement(n, '{'+ gfc +'}valueType')
                r = ET.SubElement(q, '{'+ gco +'}TypeName')
                s = ET.SubElement(r, '{'+ gco +'}aName')
                t = ET.SubElement(s, '{'+ gco +'}CharacterString')
                t.text = carrierOfCharacteristics['valueType']

                for listedValue in carrierOfCharacteristics['listedValueList']:
                    u = ET.SubElement(n, '{'+ gfc +'}listedValue')
                    v = ET.SubElement(u, '{'+ gfc +'}FC_ListedValue')
                    w = ET.SubElement(v, '{'+ gfc +'}label')
                    x = ET.SubElement(w, '{'+ gco +'}CharacterString')
                    x.text = str(listedValue)


    def coverageDescription(self, contentTypeCode, numberOfBands, maxValues, minValues, noDataValue):
        a = ET.SubElement(self.root, '{'+ mdb +'}contentInfo')
        b = ET.SubElement(a, '{'+ mrc +'}MI_CoverageDescription')
        c = ET.SubElement(b, '{'+ mrc +'}attributeDescription')
        d = ET.SubElement(c, '{'+ gco +'}RecordType')
        d.text = "Grid Cell"

        e = ET.SubElement(b, '{'+ mrc +'}attributeGroup')
        f = ET.SubElement(e, '{'+ mrc +'}MD_AttributeGroup')
        g = ET.SubElement(f, '{'+ mrc +'}contentType')
        ET.SubElement(g, '{'+ mrc +'}MD_CoverageContentTypeCode', codeList=codelist_MD_CoverageContentTypeCode, codeListValue=contentTypeCode)

        h = ET.SubElement(f, '{'+ mrc +'}attribute')
        for band_idx in range(numberOfBands):
            i = ET.SubElement(h, '{'+ mrc +'}MD_SampleDimension')
            j = ET.SubElement(i, '{'+ mrc +'}description')
            k = ET.SubElement(j, '{'+ gco +'}CharacterString')
            k.text = 'Band_' + str(band_idx+1)
            l = ET.SubElement(i, '{'+ mrc +'}maxValue')
            m = ET.SubElement(l, '{'+ gco +'}Real')
            m.text = str(maxValues[band_idx])
            n = ET.SubElement(i, '{'+ mrc +'}minValue')
            o = ET.SubElement(n, '{'+ gco +'}Real')
            o.text = str(minValues[band_idx])

        p = ET.SubElement(b, '{'+ mrc +'}rangeElementDescription')
        q = ET.SubElement(p, '{'+ mrc +'}MI_RangeElementDescription')
        r = ET.SubElement(q, '{'+ mrc +'}name')
        s = ET.SubElement(r, '{'+ gco +'}CharacterString')
        s.text = "Empty Grid Cell"
        t = ET.SubElement(q, '{'+ mrc +'}definition')
        u = ET.SubElement(t, '{'+ gco +'}CharacterString')
        u.text = "Representation of grid cell with no measurement value"
        v = ET.SubElement(q, '{'+ mrc +'}rangeElement')
        w = ET.SubElement(v, '{'+ gco +'}Record')
        x = ET.SubElement(w, '{'+ gco +'}CharacterString')
        x.text = str(noDataValue)




