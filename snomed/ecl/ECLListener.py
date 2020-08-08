# Generated from ECL.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ECLParser import ECLParser
else:
    from ECLParser import ECLParser

# This class defines a complete listener for a parse tree produced by ECLParser.
class ECLListener(ParseTreeListener):

    # Enter a parse tree produced by ECLParser#expressionconstraint.
    def enterExpressionconstraint(self, ctx:ECLParser.ExpressionconstraintContext):
        pass

    # Exit a parse tree produced by ECLParser#expressionconstraint.
    def exitExpressionconstraint(self, ctx:ECLParser.ExpressionconstraintContext):
        pass


    # Enter a parse tree produced by ECLParser#refinedexpressionconstraint.
    def enterRefinedexpressionconstraint(self, ctx:ECLParser.RefinedexpressionconstraintContext):
        pass

    # Exit a parse tree produced by ECLParser#refinedexpressionconstraint.
    def exitRefinedexpressionconstraint(self, ctx:ECLParser.RefinedexpressionconstraintContext):
        pass


    # Enter a parse tree produced by ECLParser#compoundexpressionconstraint.
    def enterCompoundexpressionconstraint(self, ctx:ECLParser.CompoundexpressionconstraintContext):
        pass

    # Exit a parse tree produced by ECLParser#compoundexpressionconstraint.
    def exitCompoundexpressionconstraint(self, ctx:ECLParser.CompoundexpressionconstraintContext):
        pass


    # Enter a parse tree produced by ECLParser#conjunctionexpressionconstraint.
    def enterConjunctionexpressionconstraint(self, ctx:ECLParser.ConjunctionexpressionconstraintContext):
        pass

    # Exit a parse tree produced by ECLParser#conjunctionexpressionconstraint.
    def exitConjunctionexpressionconstraint(self, ctx:ECLParser.ConjunctionexpressionconstraintContext):
        pass


    # Enter a parse tree produced by ECLParser#disjunctionexpressionconstraint.
    def enterDisjunctionexpressionconstraint(self, ctx:ECLParser.DisjunctionexpressionconstraintContext):
        pass

    # Exit a parse tree produced by ECLParser#disjunctionexpressionconstraint.
    def exitDisjunctionexpressionconstraint(self, ctx:ECLParser.DisjunctionexpressionconstraintContext):
        pass


    # Enter a parse tree produced by ECLParser#exclusionexpressionconstraint.
    def enterExclusionexpressionconstraint(self, ctx:ECLParser.ExclusionexpressionconstraintContext):
        pass

    # Exit a parse tree produced by ECLParser#exclusionexpressionconstraint.
    def exitExclusionexpressionconstraint(self, ctx:ECLParser.ExclusionexpressionconstraintContext):
        pass


    # Enter a parse tree produced by ECLParser#dottedexpressionconstraint.
    def enterDottedexpressionconstraint(self, ctx:ECLParser.DottedexpressionconstraintContext):
        pass

    # Exit a parse tree produced by ECLParser#dottedexpressionconstraint.
    def exitDottedexpressionconstraint(self, ctx:ECLParser.DottedexpressionconstraintContext):
        pass


    # Enter a parse tree produced by ECLParser#dottedexpressionattribute.
    def enterDottedexpressionattribute(self, ctx:ECLParser.DottedexpressionattributeContext):
        pass

    # Exit a parse tree produced by ECLParser#dottedexpressionattribute.
    def exitDottedexpressionattribute(self, ctx:ECLParser.DottedexpressionattributeContext):
        pass


    # Enter a parse tree produced by ECLParser#subexpressionconstraint.
    def enterSubexpressionconstraint(self, ctx:ECLParser.SubexpressionconstraintContext):
        pass

    # Exit a parse tree produced by ECLParser#subexpressionconstraint.
    def exitSubexpressionconstraint(self, ctx:ECLParser.SubexpressionconstraintContext):
        pass


    # Enter a parse tree produced by ECLParser#eclfocusconcept.
    def enterEclfocusconcept(self, ctx:ECLParser.EclfocusconceptContext):
        pass

    # Exit a parse tree produced by ECLParser#eclfocusconcept.
    def exitEclfocusconcept(self, ctx:ECLParser.EclfocusconceptContext):
        pass


    # Enter a parse tree produced by ECLParser#dot.
    def enterDot(self, ctx:ECLParser.DotContext):
        pass

    # Exit a parse tree produced by ECLParser#dot.
    def exitDot(self, ctx:ECLParser.DotContext):
        pass


    # Enter a parse tree produced by ECLParser#memberof.
    def enterMemberof(self, ctx:ECLParser.MemberofContext):
        pass

    # Exit a parse tree produced by ECLParser#memberof.
    def exitMemberof(self, ctx:ECLParser.MemberofContext):
        pass


    # Enter a parse tree produced by ECLParser#eclconceptreference.
    def enterEclconceptreference(self, ctx:ECLParser.EclconceptreferenceContext):
        pass

    # Exit a parse tree produced by ECLParser#eclconceptreference.
    def exitEclconceptreference(self, ctx:ECLParser.EclconceptreferenceContext):
        pass


    # Enter a parse tree produced by ECLParser#conceptid.
    def enterConceptid(self, ctx:ECLParser.ConceptidContext):
        pass

    # Exit a parse tree produced by ECLParser#conceptid.
    def exitConceptid(self, ctx:ECLParser.ConceptidContext):
        pass


    # Enter a parse tree produced by ECLParser#term.
    def enterTerm(self, ctx:ECLParser.TermContext):
        pass

    # Exit a parse tree produced by ECLParser#term.
    def exitTerm(self, ctx:ECLParser.TermContext):
        pass


    # Enter a parse tree produced by ECLParser#wildcard.
    def enterWildcard(self, ctx:ECLParser.WildcardContext):
        pass

    # Exit a parse tree produced by ECLParser#wildcard.
    def exitWildcard(self, ctx:ECLParser.WildcardContext):
        pass


    # Enter a parse tree produced by ECLParser#constraintoperator.
    def enterConstraintoperator(self, ctx:ECLParser.ConstraintoperatorContext):
        pass

    # Exit a parse tree produced by ECLParser#constraintoperator.
    def exitConstraintoperator(self, ctx:ECLParser.ConstraintoperatorContext):
        pass


    # Enter a parse tree produced by ECLParser#descendantof.
    def enterDescendantof(self, ctx:ECLParser.DescendantofContext):
        pass

    # Exit a parse tree produced by ECLParser#descendantof.
    def exitDescendantof(self, ctx:ECLParser.DescendantofContext):
        pass


    # Enter a parse tree produced by ECLParser#descendantorselfof.
    def enterDescendantorselfof(self, ctx:ECLParser.DescendantorselfofContext):
        pass

    # Exit a parse tree produced by ECLParser#descendantorselfof.
    def exitDescendantorselfof(self, ctx:ECLParser.DescendantorselfofContext):
        pass


    # Enter a parse tree produced by ECLParser#childof.
    def enterChildof(self, ctx:ECLParser.ChildofContext):
        pass

    # Exit a parse tree produced by ECLParser#childof.
    def exitChildof(self, ctx:ECLParser.ChildofContext):
        pass


    # Enter a parse tree produced by ECLParser#ancestorof.
    def enterAncestorof(self, ctx:ECLParser.AncestorofContext):
        pass

    # Exit a parse tree produced by ECLParser#ancestorof.
    def exitAncestorof(self, ctx:ECLParser.AncestorofContext):
        pass


    # Enter a parse tree produced by ECLParser#ancestororselfof.
    def enterAncestororselfof(self, ctx:ECLParser.AncestororselfofContext):
        pass

    # Exit a parse tree produced by ECLParser#ancestororselfof.
    def exitAncestororselfof(self, ctx:ECLParser.AncestororselfofContext):
        pass


    # Enter a parse tree produced by ECLParser#parentof.
    def enterParentof(self, ctx:ECLParser.ParentofContext):
        pass

    # Exit a parse tree produced by ECLParser#parentof.
    def exitParentof(self, ctx:ECLParser.ParentofContext):
        pass


    # Enter a parse tree produced by ECLParser#conjunction.
    def enterConjunction(self, ctx:ECLParser.ConjunctionContext):
        pass

    # Exit a parse tree produced by ECLParser#conjunction.
    def exitConjunction(self, ctx:ECLParser.ConjunctionContext):
        pass


    # Enter a parse tree produced by ECLParser#disjunction.
    def enterDisjunction(self, ctx:ECLParser.DisjunctionContext):
        pass

    # Exit a parse tree produced by ECLParser#disjunction.
    def exitDisjunction(self, ctx:ECLParser.DisjunctionContext):
        pass


    # Enter a parse tree produced by ECLParser#exclusion.
    def enterExclusion(self, ctx:ECLParser.ExclusionContext):
        pass

    # Exit a parse tree produced by ECLParser#exclusion.
    def exitExclusion(self, ctx:ECLParser.ExclusionContext):
        pass


    # Enter a parse tree produced by ECLParser#eclrefinement.
    def enterEclrefinement(self, ctx:ECLParser.EclrefinementContext):
        pass

    # Exit a parse tree produced by ECLParser#eclrefinement.
    def exitEclrefinement(self, ctx:ECLParser.EclrefinementContext):
        pass


    # Enter a parse tree produced by ECLParser#conjunctionrefinementset.
    def enterConjunctionrefinementset(self, ctx:ECLParser.ConjunctionrefinementsetContext):
        pass

    # Exit a parse tree produced by ECLParser#conjunctionrefinementset.
    def exitConjunctionrefinementset(self, ctx:ECLParser.ConjunctionrefinementsetContext):
        pass


    # Enter a parse tree produced by ECLParser#disjunctionrefinementset.
    def enterDisjunctionrefinementset(self, ctx:ECLParser.DisjunctionrefinementsetContext):
        pass

    # Exit a parse tree produced by ECLParser#disjunctionrefinementset.
    def exitDisjunctionrefinementset(self, ctx:ECLParser.DisjunctionrefinementsetContext):
        pass


    # Enter a parse tree produced by ECLParser#subrefinement.
    def enterSubrefinement(self, ctx:ECLParser.SubrefinementContext):
        pass

    # Exit a parse tree produced by ECLParser#subrefinement.
    def exitSubrefinement(self, ctx:ECLParser.SubrefinementContext):
        pass


    # Enter a parse tree produced by ECLParser#eclattributeset.
    def enterEclattributeset(self, ctx:ECLParser.EclattributesetContext):
        pass

    # Exit a parse tree produced by ECLParser#eclattributeset.
    def exitEclattributeset(self, ctx:ECLParser.EclattributesetContext):
        pass


    # Enter a parse tree produced by ECLParser#conjunctionattributeset.
    def enterConjunctionattributeset(self, ctx:ECLParser.ConjunctionattributesetContext):
        pass

    # Exit a parse tree produced by ECLParser#conjunctionattributeset.
    def exitConjunctionattributeset(self, ctx:ECLParser.ConjunctionattributesetContext):
        pass


    # Enter a parse tree produced by ECLParser#disjunctionattributeset.
    def enterDisjunctionattributeset(self, ctx:ECLParser.DisjunctionattributesetContext):
        pass

    # Exit a parse tree produced by ECLParser#disjunctionattributeset.
    def exitDisjunctionattributeset(self, ctx:ECLParser.DisjunctionattributesetContext):
        pass


    # Enter a parse tree produced by ECLParser#subattributeset.
    def enterSubattributeset(self, ctx:ECLParser.SubattributesetContext):
        pass

    # Exit a parse tree produced by ECLParser#subattributeset.
    def exitSubattributeset(self, ctx:ECLParser.SubattributesetContext):
        pass


    # Enter a parse tree produced by ECLParser#eclattributegroup.
    def enterEclattributegroup(self, ctx:ECLParser.EclattributegroupContext):
        pass

    # Exit a parse tree produced by ECLParser#eclattributegroup.
    def exitEclattributegroup(self, ctx:ECLParser.EclattributegroupContext):
        pass


    # Enter a parse tree produced by ECLParser#eclattribute.
    def enterEclattribute(self, ctx:ECLParser.EclattributeContext):
        pass

    # Exit a parse tree produced by ECLParser#eclattribute.
    def exitEclattribute(self, ctx:ECLParser.EclattributeContext):
        pass


    # Enter a parse tree produced by ECLParser#cardinality.
    def enterCardinality(self, ctx:ECLParser.CardinalityContext):
        pass

    # Exit a parse tree produced by ECLParser#cardinality.
    def exitCardinality(self, ctx:ECLParser.CardinalityContext):
        pass


    # Enter a parse tree produced by ECLParser#minvalue.
    def enterMinvalue(self, ctx:ECLParser.MinvalueContext):
        pass

    # Exit a parse tree produced by ECLParser#minvalue.
    def exitMinvalue(self, ctx:ECLParser.MinvalueContext):
        pass


    # Enter a parse tree produced by ECLParser#to.
    def enterTo(self, ctx:ECLParser.ToContext):
        pass

    # Exit a parse tree produced by ECLParser#to.
    def exitTo(self, ctx:ECLParser.ToContext):
        pass


    # Enter a parse tree produced by ECLParser#maxvalue.
    def enterMaxvalue(self, ctx:ECLParser.MaxvalueContext):
        pass

    # Exit a parse tree produced by ECLParser#maxvalue.
    def exitMaxvalue(self, ctx:ECLParser.MaxvalueContext):
        pass


    # Enter a parse tree produced by ECLParser#many.
    def enterMany(self, ctx:ECLParser.ManyContext):
        pass

    # Exit a parse tree produced by ECLParser#many.
    def exitMany(self, ctx:ECLParser.ManyContext):
        pass


    # Enter a parse tree produced by ECLParser#reverseflag.
    def enterReverseflag(self, ctx:ECLParser.ReverseflagContext):
        pass

    # Exit a parse tree produced by ECLParser#reverseflag.
    def exitReverseflag(self, ctx:ECLParser.ReverseflagContext):
        pass


    # Enter a parse tree produced by ECLParser#eclattributename.
    def enterEclattributename(self, ctx:ECLParser.EclattributenameContext):
        pass

    # Exit a parse tree produced by ECLParser#eclattributename.
    def exitEclattributename(self, ctx:ECLParser.EclattributenameContext):
        pass


    # Enter a parse tree produced by ECLParser#expressioncomparisonoperator.
    def enterExpressioncomparisonoperator(self, ctx:ECLParser.ExpressioncomparisonoperatorContext):
        pass

    # Exit a parse tree produced by ECLParser#expressioncomparisonoperator.
    def exitExpressioncomparisonoperator(self, ctx:ECLParser.ExpressioncomparisonoperatorContext):
        pass


    # Enter a parse tree produced by ECLParser#numericcomparisonoperator.
    def enterNumericcomparisonoperator(self, ctx:ECLParser.NumericcomparisonoperatorContext):
        pass

    # Exit a parse tree produced by ECLParser#numericcomparisonoperator.
    def exitNumericcomparisonoperator(self, ctx:ECLParser.NumericcomparisonoperatorContext):
        pass


    # Enter a parse tree produced by ECLParser#stringcomparisonoperator.
    def enterStringcomparisonoperator(self, ctx:ECLParser.StringcomparisonoperatorContext):
        pass

    # Exit a parse tree produced by ECLParser#stringcomparisonoperator.
    def exitStringcomparisonoperator(self, ctx:ECLParser.StringcomparisonoperatorContext):
        pass


    # Enter a parse tree produced by ECLParser#numericvalue.
    def enterNumericvalue(self, ctx:ECLParser.NumericvalueContext):
        pass

    # Exit a parse tree produced by ECLParser#numericvalue.
    def exitNumericvalue(self, ctx:ECLParser.NumericvalueContext):
        pass


    # Enter a parse tree produced by ECLParser#stringvalue.
    def enterStringvalue(self, ctx:ECLParser.StringvalueContext):
        pass

    # Exit a parse tree produced by ECLParser#stringvalue.
    def exitStringvalue(self, ctx:ECLParser.StringvalueContext):
        pass


    # Enter a parse tree produced by ECLParser#integervalue.
    def enterIntegervalue(self, ctx:ECLParser.IntegervalueContext):
        pass

    # Exit a parse tree produced by ECLParser#integervalue.
    def exitIntegervalue(self, ctx:ECLParser.IntegervalueContext):
        pass


    # Enter a parse tree produced by ECLParser#decimalvalue.
    def enterDecimalvalue(self, ctx:ECLParser.DecimalvalueContext):
        pass

    # Exit a parse tree produced by ECLParser#decimalvalue.
    def exitDecimalvalue(self, ctx:ECLParser.DecimalvalueContext):
        pass


    # Enter a parse tree produced by ECLParser#nonnegativeintegervalue.
    def enterNonnegativeintegervalue(self, ctx:ECLParser.NonnegativeintegervalueContext):
        pass

    # Exit a parse tree produced by ECLParser#nonnegativeintegervalue.
    def exitNonnegativeintegervalue(self, ctx:ECLParser.NonnegativeintegervalueContext):
        pass


    # Enter a parse tree produced by ECLParser#sctid.
    def enterSctid(self, ctx:ECLParser.SctidContext):
        pass

    # Exit a parse tree produced by ECLParser#sctid.
    def exitSctid(self, ctx:ECLParser.SctidContext):
        pass


    # Enter a parse tree produced by ECLParser#ws.
    def enterWs(self, ctx:ECLParser.WsContext):
        pass

    # Exit a parse tree produced by ECLParser#ws.
    def exitWs(self, ctx:ECLParser.WsContext):
        pass


    # Enter a parse tree produced by ECLParser#mws.
    def enterMws(self, ctx:ECLParser.MwsContext):
        pass

    # Exit a parse tree produced by ECLParser#mws.
    def exitMws(self, ctx:ECLParser.MwsContext):
        pass


    # Enter a parse tree produced by ECLParser#comment.
    def enterComment(self, ctx:ECLParser.CommentContext):
        pass

    # Exit a parse tree produced by ECLParser#comment.
    def exitComment(self, ctx:ECLParser.CommentContext):
        pass


    # Enter a parse tree produced by ECLParser#nonstarchar.
    def enterNonstarchar(self, ctx:ECLParser.NonstarcharContext):
        pass

    # Exit a parse tree produced by ECLParser#nonstarchar.
    def exitNonstarchar(self, ctx:ECLParser.NonstarcharContext):
        pass


    # Enter a parse tree produced by ECLParser#starwithnonfslash.
    def enterStarwithnonfslash(self, ctx:ECLParser.StarwithnonfslashContext):
        pass

    # Exit a parse tree produced by ECLParser#starwithnonfslash.
    def exitStarwithnonfslash(self, ctx:ECLParser.StarwithnonfslashContext):
        pass


    # Enter a parse tree produced by ECLParser#nonfslash.
    def enterNonfslash(self, ctx:ECLParser.NonfslashContext):
        pass

    # Exit a parse tree produced by ECLParser#nonfslash.
    def exitNonfslash(self, ctx:ECLParser.NonfslashContext):
        pass


    # Enter a parse tree produced by ECLParser#sp.
    def enterSp(self, ctx:ECLParser.SpContext):
        pass

    # Exit a parse tree produced by ECLParser#sp.
    def exitSp(self, ctx:ECLParser.SpContext):
        pass


    # Enter a parse tree produced by ECLParser#htab.
    def enterHtab(self, ctx:ECLParser.HtabContext):
        pass

    # Exit a parse tree produced by ECLParser#htab.
    def exitHtab(self, ctx:ECLParser.HtabContext):
        pass


    # Enter a parse tree produced by ECLParser#cr.
    def enterCr(self, ctx:ECLParser.CrContext):
        pass

    # Exit a parse tree produced by ECLParser#cr.
    def exitCr(self, ctx:ECLParser.CrContext):
        pass


    # Enter a parse tree produced by ECLParser#lf.
    def enterLf(self, ctx:ECLParser.LfContext):
        pass

    # Exit a parse tree produced by ECLParser#lf.
    def exitLf(self, ctx:ECLParser.LfContext):
        pass


    # Enter a parse tree produced by ECLParser#qm.
    def enterQm(self, ctx:ECLParser.QmContext):
        pass

    # Exit a parse tree produced by ECLParser#qm.
    def exitQm(self, ctx:ECLParser.QmContext):
        pass


    # Enter a parse tree produced by ECLParser#bs.
    def enterBs(self, ctx:ECLParser.BsContext):
        pass

    # Exit a parse tree produced by ECLParser#bs.
    def exitBs(self, ctx:ECLParser.BsContext):
        pass


    # Enter a parse tree produced by ECLParser#digit.
    def enterDigit(self, ctx:ECLParser.DigitContext):
        pass

    # Exit a parse tree produced by ECLParser#digit.
    def exitDigit(self, ctx:ECLParser.DigitContext):
        pass


    # Enter a parse tree produced by ECLParser#zero.
    def enterZero(self, ctx:ECLParser.ZeroContext):
        pass

    # Exit a parse tree produced by ECLParser#zero.
    def exitZero(self, ctx:ECLParser.ZeroContext):
        pass


    # Enter a parse tree produced by ECLParser#digitnonzero.
    def enterDigitnonzero(self, ctx:ECLParser.DigitnonzeroContext):
        pass

    # Exit a parse tree produced by ECLParser#digitnonzero.
    def exitDigitnonzero(self, ctx:ECLParser.DigitnonzeroContext):
        pass


    # Enter a parse tree produced by ECLParser#nonwsnonpipe.
    def enterNonwsnonpipe(self, ctx:ECLParser.NonwsnonpipeContext):
        pass

    # Exit a parse tree produced by ECLParser#nonwsnonpipe.
    def exitNonwsnonpipe(self, ctx:ECLParser.NonwsnonpipeContext):
        pass


    # Enter a parse tree produced by ECLParser#anynonescapedchar.
    def enterAnynonescapedchar(self, ctx:ECLParser.AnynonescapedcharContext):
        pass

    # Exit a parse tree produced by ECLParser#anynonescapedchar.
    def exitAnynonescapedchar(self, ctx:ECLParser.AnynonescapedcharContext):
        pass


    # Enter a parse tree produced by ECLParser#escapedchar.
    def enterEscapedchar(self, ctx:ECLParser.EscapedcharContext):
        pass

    # Exit a parse tree produced by ECLParser#escapedchar.
    def exitEscapedchar(self, ctx:ECLParser.EscapedcharContext):
        pass


