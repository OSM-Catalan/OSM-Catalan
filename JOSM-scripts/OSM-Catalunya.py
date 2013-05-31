#!/bin/jython
'''
OSM-CAT-fix-places.jy

Proof of concept JOSM script to fix name in selected nodes/way/relations.

This code is released under the GNU General
Public License v2 or later.

The GPL v3 is accessible here:
http://www.gnu.org/licenses/gpl.html

The GPL v2 is accessible here:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

It comes with no warranty whatsoever.


'''
from javax.swing import JOptionPane
from org.openstreetmap.josm import Main
import org.openstreetmap.josm.command as Command
import org.openstreetmap.josm.data.osm.Node as Node
import org.openstreetmap.josm.data.osm.Way as Way
import org.openstreetmap.josm.data.osm.Relation as Relation
import org.openstreetmap.josm.data.osm.TagCollection as TagCollection
import org.openstreetmap.josm.data.osm.DataSet as DataSet
import org.openstreetmap.josm.data.osm.RelationMember as RelationMember
import org.openstreetmap.josm.gui.dialogs.relation.DownloadRelationMemberTask as DownloadRelationMemberTask
import org.openstreetmap.josm.actions.DownloadReferrersAction as DownloadReferrersAction
import org.openstreetmap.josm.actions.AutoScaleAction as AutoScaleAction
import re, time
import codecs


logVerbosity = 50
'''
10: only report problems that require attention
20: report on collection
30: report on network nodes
40: report on which routes are being checked
50: report everything
'''

forceNameCA = False
'''
if True name:ca will be same as name on checked nodes/ways/relations
'''

def getMapView():
    if Main.main and Main.main.map:
        return Main.main.map.mapView
    else:
        return None



dummy_node = Node()
dummy_way = Way()
dummy_relation = Relation()
commandsList = []

pattern = re.compile("^(L'|El |La |Els |Les |Los |Lo |S'|Es |Sa |Ses )")

mv = getMapView()

if mv and mv.editLayer and mv.editLayer.data:
    selectedNodes = mv.editLayer.data.getSelectedNodes()
    selectedWays = mv.editLayer.data.getSelectedWays()
    selectedRelations = mv.editLayer.data.getSelectedRelations()

    if not(selectedNodes or selectedWays or selectedRelations):
        JOptionPane.showMessageDialog(Main.parent, "Please select some node, way, or relation.")
    else:
    
        if (selectedNodes):

	        for node in selectedNodes:
	        	nodeChanged = False
	        	oldname = node.get('name')
	        	if not(oldname): oldname = ''
	        	if pattern.match(oldname):
	        		newNode = Node(node)
	        		newname = oldname
		        	newname = re.sub("^E","e", newname)
		        	newname = re.sub("^L","l", newname)
		        	newname = re.sub("^S","s", newname)
		        	newNode.put("name", newname)
		        	if (forceNameCA): newNode.put("name:ca", newname)
		        	
		        	commandsList.append(Command.ChangeCommand(node, newNode))
		        	Main.main.undoRedo.add(Command.SequenceCommand("Changed name "+oldname, commandsList))
		        	commandsList = []
		
        if (selectedWays):
			JOptionPane.showMessageDialog(Main.parent, "You have selected some way.")
        if (selectedRelations):
	    	JOptionPane.showMessageDialog(Main.parent, "You have selected some relation.")
			


