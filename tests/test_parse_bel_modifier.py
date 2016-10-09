import logging

from pybel.parser.test_utils import TestTokenParserBase

log = logging.getLogger(__name__)


class TestActivity(TestTokenParserBase):
    def test_activity_bare(self):
        """"""
        statement = 'act(p(HGNC:AKT1))'
        result = self.parser.activity.parseString(statement)

        expected_result = ['Activity', ['Protein', ['HGNC', 'AKT1']]]
        self.assertEqual(expected_result, result.asList())

        mod = self.parser.canonicalize_modifier(result)
        expected_mod = {
            'modifier': 'Activity',
            'effect': {}
        }
        self.assertEqual(expected_mod, mod)

    def test_activity_withMolecularActivityDefault(self):
        """Tests activity modifier with molecular activity from default BEL namespace"""
        statement = 'act(p(HGNC:AKT1), ma(kin))'
        result = self.parser.activity.parseString(statement)

        expected_dict = {
            'modifier': 'Activity',
            'effect': {
                'MolecularActivity': 'KinaseActivity'
            },
            'target': {
                'function': 'Protein',
                'identifier': dict(namespace='HGNC', name='AKT1')
            }
        }
        self.assertEqual(expected_dict, result.asDict())

        mod = self.parser.canonicalize_modifier(result)
        expected_mod = {
            'modifier': 'Activity',
            'effect': {
                'MolecularActivity': 'KinaseActivity'
            }
        }
        self.assertEqual(expected_mod, mod)

    def test_activity_withMolecularActivityCustom(self):
        """Tests activity modifier with molecular activity from custom namespaced"""
        statement = 'act(p(HGNC:AKT1), ma(GOMF:"catalytic activity"))'
        result = self.parser.activity.parseString(statement)

        expected_dict = {
            'modifier': 'Activity',
            'effect': {
                'MolecularActivity': dict(namespace='GOMF', name='catalytic activity')
            },
            'target': {
                'function': 'Protein',
                'identifier': dict(namespace='HGNC', name='AKT1')
            }
        }
        self.assertEqual(expected_dict, result.asDict())

        mod = self.parser.canonicalize_modifier(result)
        expected_mod = {
            'modifier': 'Activity',
            'effect': {
                'MolecularActivity': dict(namespace='GOMF', name='catalytic activity')
            }
        }
        self.assertEqual(expected_mod, mod)

    def test_activity_legacy(self):
        """Test BEL 1.0 style molecular activity annotation"""
        statement = 'kin(p(HGNC:AKT1))'
        result = self.parser.activity.parseString(statement)

        # expected_result = ['Activity', ['Protein', ['HGNC', 'AKT1']], ['MolecularActivity', 'KinaseActivity']]
        # self.assertEqual(expected_result, result.asList())

        print(result.asDict())

        expected_dict = {
            'modifier': 'Activity',
            'effect': {
                'MolecularActivity': 'KinaseActivity'
            },
            'target': {
                'function': 'Protein',
                'identifier': dict(namespace='HGNC', name='AKT1')
            }
        }
        self.assertEqual(expected_dict, result.asDict())

        mod = self.parser.canonicalize_modifier(result)
        expected_mod = {
            'modifier': 'Activity',
            'effect': {
                'MolecularActivity': 'KinaseActivity'
            }
        }
        self.assertEqual(expected_mod, mod)

        node = 'Protein', 'HGNC', 'AKT1'
        self.assertEqual(node, self.parser.canonicalize_node(result))
        self.assertHasNode(node)


class TestTransformation(TestTokenParserBase):
    def test_degredation_1(self):
        statement = 'deg(p(HGNC:AKT1))'
        result = self.parser.transformation.parseString(statement)

        expected_result = ['Degradation', ['Protein', ['HGNC', 'AKT1']]]
        self.assertEqual(expected_result, result.asList())

        expected_dict = {
            'modifier': 'Degradation',
            'target': {
                'function': 'Protein',
                'identifier': dict(namespace='HGNC', name='AKT1')
            }
        }
        self.assertEqual(expected_dict, result.asDict())

        mod = self.parser.canonicalize_modifier(result)
        expected_mod = {
            'modifier': 'Degradation',
        }
        self.assertEqual(expected_mod, mod)

    def test_degradation_2(self):
        """"""
        statement = 'deg(p(HGNC:EGFR))'
        result = self.parser.transformation.parseString(statement)

        expected_result = ['Degradation', ['Protein', ['HGNC', 'EGFR']]]
        self.assertEqual(expected_result, result.asList())

        expected_dict = {
            'modifier': 'Degradation',
            'target': {
                'function': 'Protein',
                'identifier': dict(namespace='HGNC', name='EGFR')
            }
        }
        self.assertEqual(expected_dict, result.asDict())

        mod = self.parser.canonicalize_modifier(result)
        expected_mod = {
            'modifier': 'Degradation',
        }
        self.assertEqual(expected_mod, mod)

        node = 'Protein', 'HGNC', 'EGFR'
        self.assertEqual(node, self.parser.canonicalize_node(result))
        self.assertHasNode(node)

    def test_translocation_standard(self):
        """translocation example"""
        statement = 'tloc(p(HGNC:EGFR), fromLoc(GOCC:"cell surface"), toLoc(GOCC:endosome))'
        result = self.parser.translocation.parseString(statement)

        expected_dict = {
            'modifier': 'Translocation',
            'target': {
                'function': 'Protein',
                'identifier': dict(namespace='HGNC', name='EGFR')
            },
            'effect': {
                'fromLoc': dict(namespace='GOCC', name='cell surface'),
                'toLoc': dict(namespace='GOCC', name='endosome')
            }
        }

        self.assertEqual(expected_dict, result.asDict())

        mod = self.parser.canonicalize_modifier(result)
        expected_mod = {
            'modifier': 'Translocation',
            'effect': {
                'fromLoc': dict(namespace='GOCC', name='cell surface'),
                'toLoc': dict(namespace='GOCC', name='endosome')
            }
        }
        self.assertEqual(expected_mod, mod)

        node = 'Protein', 'HGNC', 'EGFR'
        self.assertEqual(node, self.parser.canonicalize_node(result))
        self.assertHasNode(node)

    def test_translocation_bare(self):
        """translocation example"""
        statement = 'tloc(p(HGNC:EGFR), GOCC:"cell surface", GOCC:endosome)'
        result = self.parser.translocation.parseString(statement)

        expected_dict = {
            'modifier': 'Translocation',
            'target': {
                'function': 'Protein',
                'identifier': dict(namespace='HGNC', name='EGFR')
            },
            'effect': {
                'fromLoc': dict(namespace='GOCC', name='cell surface'),
                'toLoc': dict(namespace='GOCC', name='endosome')
            }
        }
        self.assertEqual(expected_dict, result.asDict())

        mod = self.parser.canonicalize_modifier(result)
        expected_mod = {
            'modifier': 'Translocation',
            'effect': {
                'fromLoc': dict(namespace='GOCC', name='cell surface'),
                'toLoc': dict(namespace='GOCC', name='endosome')
            }
        }
        self.assertEqual(expected_mod, mod)

        node = 'Protein', 'HGNC', 'EGFR'
        self.assertEqual(node, self.parser.canonicalize_node(result))
        self.assertHasNode(node)

    def test_translocation_invalid(self):
        """Fail on an improperly written single argument translocation"""
        statement = 'tloc(a("T-Lymphocytes"))'
        with self.assertRaises(Exception):
            self.parser.translocation.parseString(statement)

    def test_translocation_secretion(self):
        """cell secretion short form"""
        statement = 'sec(p(HGNC:EGFR))'
        result = self.parser.transformation.parseString(statement)

        expected_result = ['CellSecretion', ['Protein', ['HGNC', 'EGFR']]]
        self.assertEqual(expected_result, result.asList())

        mod = self.parser.canonicalize_modifier(result)
        expected_mod = {
            'modifier': 'Translocation',
            'effect': {
                'fromLoc': dict(namespace='GOCC', name='intracellular'),
                'toLoc': dict(namespace='GOCC', name='extracellular space')
            }
        }
        self.assertEqual(expected_mod, mod)

        node = 'Protein', 'HGNC', 'EGFR'
        self.assertEqual(node, self.parser.canonicalize_node(result))
        self.assertHasNode(node)

    def test_translocation_surface(self):
        """cell surface expression short form"""
        statement = 'surf(p(HGNC:EGFR))'
        result = self.parser.transformation.parseString(statement)

        expected_result = ['CellSurfaceExpression', ['Protein', ['HGNC', 'EGFR']]]
        self.assertEqual(expected_result, result.asList())

        mod = self.parser.canonicalize_modifier(result)
        expected_mod = {
            'modifier': 'Translocation',
            'effect': {
                'fromLoc': dict(namespace='GOCC', name='intracellular'),
                'toLoc': dict(namespace='GOCC', name='cell surface')
            }
        }
        self.assertEqual(expected_mod, mod)

        node = 'Protein', 'HGNC', 'EGFR'
        self.assertEqual(node, self.parser.canonicalize_node(result))
        self.assertHasNode(node)

    def test_reaction_1(self):
        """"""
        statement = 'rxn(reactants(a(CHEBI:superoxide)),products(a(CHEBI:"hydrogen peroxide"), a(CHEBI:"oxygen")))'
        result = self.parser.transformation.parseString(statement)
        print(result.asDict())
        expected_result = [
            'Reaction',
            [['Abundance', ['CHEBI', 'superoxide']]],
            [['Abundance', ['CHEBI', 'hydrogen peroxide']], ['Abundance', ['CHEBI', 'oxygen']]]
        ]
        self.assertEqual(expected_result, result.asList())

        expected_dict = {
            'transformation': 'Reaction',
            'reactants': [
                {
                    'function': 'Abundance',
                    'identifier': dict(namespace='CHEBI', name='superoxide')
                }
            ],
            'products': [
                {
                    'function': 'Abundance',
                    'identifier': dict(namespace='CHEBI', name='hydrogen peroxide')
                }, {

                    'function': 'Abundance',
                    'identifier': dict(namespace='CHEBI', name='oxygen')
                }

            ]
        }
        self.assertEqual(expected_dict, result.asDict())

        print('N2ID', self.parser.node_to_id)

        node = 'Reaction', 1
        self.assertEqual(node, self.parser.canonicalize_node(result))
        self.assertHasNode(node)

        self.assertHasNode(('Abundance', 'CHEBI', 'superoxide'))
        self.assertHasEdge(node, ('Abundance', 'CHEBI', 'superoxide'))

        self.assertHasNode(('Abundance', 'CHEBI', 'hydrogen peroxide'))
        self.assertHasEdge(node, ('Abundance', 'CHEBI', 'hydrogen peroxide'))

        self.assertHasNode(('Abundance', 'CHEBI', 'oxygen'))
        self.assertHasEdge(node, ('Abundance', 'CHEBI', 'oxygen'))