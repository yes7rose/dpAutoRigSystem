# importing libraries:
import maya.cmds as cmds
import dpAutoRigSystem.Controls.dpBaseControlClass as BaseControl
reload(BaseControl)

# global variables to this module:    
CLASS_NAME = "Arrow"
TITLE = "m113_arrow"
DESCRIPTION = "m099_cvControlDesc"
ICON = "/Icons/dp_arrow.png"

dpArrowVersion = 1.0

class Arrow(BaseControl.ControlStartClass):
    def __init__(self, *args, **kwargs):
        #Add the needed parameter to the kwargs dict to be able to maintain the parameter order
        kwargs["CLASS_NAME"] = CLASS_NAME
        kwargs["TITLE"] = TITLE
        kwargs["DESCRIPTION"] = DESCRIPTION
        kwargs["ICON"] = ICON
        BaseControl.ControlStartClass.__init__(self, *args, **kwargs)
        # dependence module list:
        self.checkModuleList = ['dpArrowFlat']
    
    
    def cvMain(self, useUI, cvID=None, cvName=CLASS_NAME+'_Ctrl', cvSize=1.0, cvDegree=1, cvDirection='+Y', cvAction=1, dpGuide=False, *args):
        """ The principal method to call all other methods in order to build the cvControl curve.
            Return the result: new control curve or the destination list depending of action.
        """
        # check modules integrity:
        checkResultList = self.dpUIinst.startGuideModules(self.controlsGuideDir, "check", None, checkModuleList=self.checkModuleList)
        if len(checkResultList) == 0:
            # call combine function:
            result = self.cvCreate(useUI, cvID, cvName, cvSize, cvDegree, cvDirection, cvAction, dpGuide, True)
            return result
        else:
            # error checking modules in the folder:
            mel.eval('error \"'+ self.langDic[self.langName]['e001_GuideNotChecked'] +' - '+ (", ").join(checkResultList) +'\";')
    
    
    def generateCombineCurves(self, useUI, cvID, cvName, cvSize, cvDegree, cvDirection, *args):
        """ Combine controls in order to return it.
        """
        # load module instance
        arrowFlatInstance = self.dpUIinst.initControlModule('dpArrowFlat', self.controlsGuideDir)
        # creating curve shapes:
        curve1 = arrowFlatInstance.cvMain(useUI, cvID, cvName, cvSize, cvDegree)
        curve2 = arrowFlatInstance.cvMain(useUI, cvID, cvName, cvSize, cvDegree)
        cmds.setAttr(curve2+".rotate"+cvDirection[1], 90)
        mainCurve = self.combineCurves([curve1, curve2])
        return mainCurve