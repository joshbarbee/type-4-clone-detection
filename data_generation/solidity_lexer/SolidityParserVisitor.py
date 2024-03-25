# Generated from SolidityParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .SolidityParser import SolidityParser
else:
    from SolidityParser import SolidityParser

# This class defines a complete generic visitor for a parse tree produced by SolidityParser.

class SolidityParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SolidityParser#sourceUnit.
    def visitSourceUnit(self, ctx:SolidityParser.SourceUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#pragmaDirective.
    def visitPragmaDirective(self, ctx:SolidityParser.PragmaDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#importDirective.
    def visitImportDirective(self, ctx:SolidityParser.ImportDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#importAliases.
    def visitImportAliases(self, ctx:SolidityParser.ImportAliasesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#path.
    def visitPath(self, ctx:SolidityParser.PathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#symbolAliases.
    def visitSymbolAliases(self, ctx:SolidityParser.SymbolAliasesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#contractDefinition.
    def visitContractDefinition(self, ctx:SolidityParser.ContractDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#interfaceDefinition.
    def visitInterfaceDefinition(self, ctx:SolidityParser.InterfaceDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#libraryDefinition.
    def visitLibraryDefinition(self, ctx:SolidityParser.LibraryDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#inheritanceSpecifierList.
    def visitInheritanceSpecifierList(self, ctx:SolidityParser.InheritanceSpecifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#inheritanceSpecifier.
    def visitInheritanceSpecifier(self, ctx:SolidityParser.InheritanceSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#contractBodyElement.
    def visitContractBodyElement(self, ctx:SolidityParser.ContractBodyElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#namedArgument.
    def visitNamedArgument(self, ctx:SolidityParser.NamedArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#callArgumentList.
    def visitCallArgumentList(self, ctx:SolidityParser.CallArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#identifierPath.
    def visitIdentifierPath(self, ctx:SolidityParser.IdentifierPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#modifierInvocation.
    def visitModifierInvocation(self, ctx:SolidityParser.ModifierInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#visibility.
    def visitVisibility(self, ctx:SolidityParser.VisibilityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#parameterList.
    def visitParameterList(self, ctx:SolidityParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:SolidityParser.ParameterDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#constructorDefinition.
    def visitConstructorDefinition(self, ctx:SolidityParser.ConstructorDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#stateMutability.
    def visitStateMutability(self, ctx:SolidityParser.StateMutabilityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#overrideSpecifier.
    def visitOverrideSpecifier(self, ctx:SolidityParser.OverrideSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:SolidityParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#modifierDefinition.
    def visitModifierDefinition(self, ctx:SolidityParser.ModifierDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#fallbackFunctionDefinition.
    def visitFallbackFunctionDefinition(self, ctx:SolidityParser.FallbackFunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#receiveFunctionDefinition.
    def visitReceiveFunctionDefinition(self, ctx:SolidityParser.ReceiveFunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#structDefinition.
    def visitStructDefinition(self, ctx:SolidityParser.StructDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#structMember.
    def visitStructMember(self, ctx:SolidityParser.StructMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#enumDefinition.
    def visitEnumDefinition(self, ctx:SolidityParser.EnumDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#userDefinedValueTypeDefinition.
    def visitUserDefinedValueTypeDefinition(self, ctx:SolidityParser.UserDefinedValueTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#stateVariableDeclaration.
    def visitStateVariableDeclaration(self, ctx:SolidityParser.StateVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#constantVariableDeclaration.
    def visitConstantVariableDeclaration(self, ctx:SolidityParser.ConstantVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#eventParameter.
    def visitEventParameter(self, ctx:SolidityParser.EventParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#eventDefinition.
    def visitEventDefinition(self, ctx:SolidityParser.EventDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#errorParameter.
    def visitErrorParameter(self, ctx:SolidityParser.ErrorParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#errorDefinition.
    def visitErrorDefinition(self, ctx:SolidityParser.ErrorDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#userDefinableOperator.
    def visitUserDefinableOperator(self, ctx:SolidityParser.UserDefinableOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#usingDirective.
    def visitUsingDirective(self, ctx:SolidityParser.UsingDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#usingAliases.
    def visitUsingAliases(self, ctx:SolidityParser.UsingAliasesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#typeName.
    def visitTypeName(self, ctx:SolidityParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#elementaryTypeName.
    def visitElementaryTypeName(self, ctx:SolidityParser.ElementaryTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#functionTypeName.
    def visitFunctionTypeName(self, ctx:SolidityParser.FunctionTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:SolidityParser.VariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#dataLocation.
    def visitDataLocation(self, ctx:SolidityParser.DataLocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#UnaryPrefixOperation.
    def visitUnaryPrefixOperation(self, ctx:SolidityParser.UnaryPrefixOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#PrimaryExpression.
    def visitPrimaryExpression(self, ctx:SolidityParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#OrderComparison.
    def visitOrderComparison(self, ctx:SolidityParser.OrderComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#Conditional.
    def visitConditional(self, ctx:SolidityParser.ConditionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#PayableConversion.
    def visitPayableConversion(self, ctx:SolidityParser.PayableConversionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#Assignment.
    def visitAssignment(self, ctx:SolidityParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#UnarySuffixOperation.
    def visitUnarySuffixOperation(self, ctx:SolidityParser.UnarySuffixOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#ShiftOperation.
    def visitShiftOperation(self, ctx:SolidityParser.ShiftOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#BitAndOperation.
    def visitBitAndOperation(self, ctx:SolidityParser.BitAndOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#FunctionCall.
    def visitFunctionCall(self, ctx:SolidityParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#IndexRangeAccess.
    def visitIndexRangeAccess(self, ctx:SolidityParser.IndexRangeAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#IndexAccess.
    def visitIndexAccess(self, ctx:SolidityParser.IndexAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#AddSubOperation.
    def visitAddSubOperation(self, ctx:SolidityParser.AddSubOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#BitOrOperation.
    def visitBitOrOperation(self, ctx:SolidityParser.BitOrOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#ExpOperation.
    def visitExpOperation(self, ctx:SolidityParser.ExpOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#AndOperation.
    def visitAndOperation(self, ctx:SolidityParser.AndOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#InlineArray.
    def visitInlineArray(self, ctx:SolidityParser.InlineArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#OrOperation.
    def visitOrOperation(self, ctx:SolidityParser.OrOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#MemberAccess.
    def visitMemberAccess(self, ctx:SolidityParser.MemberAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#MulDivModOperation.
    def visitMulDivModOperation(self, ctx:SolidityParser.MulDivModOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#FunctionCallOptions.
    def visitFunctionCallOptions(self, ctx:SolidityParser.FunctionCallOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#NewExpr.
    def visitNewExpr(self, ctx:SolidityParser.NewExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#BitXorOperation.
    def visitBitXorOperation(self, ctx:SolidityParser.BitXorOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#Tuple.
    def visitTuple(self, ctx:SolidityParser.TupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#EqualityComparison.
    def visitEqualityComparison(self, ctx:SolidityParser.EqualityComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#MetaType.
    def visitMetaType(self, ctx:SolidityParser.MetaTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#assignOp.
    def visitAssignOp(self, ctx:SolidityParser.AssignOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#tupleExpression.
    def visitTupleExpression(self, ctx:SolidityParser.TupleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#inlineArrayExpression.
    def visitInlineArrayExpression(self, ctx:SolidityParser.InlineArrayExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#identifier.
    def visitIdentifier(self, ctx:SolidityParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#literal.
    def visitLiteral(self, ctx:SolidityParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#literalWithSubDenomination.
    def visitLiteralWithSubDenomination(self, ctx:SolidityParser.LiteralWithSubDenominationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:SolidityParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#stringLiteral.
    def visitStringLiteral(self, ctx:SolidityParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#hexStringLiteral.
    def visitHexStringLiteral(self, ctx:SolidityParser.HexStringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#unicodeStringLiteral.
    def visitUnicodeStringLiteral(self, ctx:SolidityParser.UnicodeStringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#numberLiteral.
    def visitNumberLiteral(self, ctx:SolidityParser.NumberLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#block.
    def visitBlock(self, ctx:SolidityParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#uncheckedBlock.
    def visitUncheckedBlock(self, ctx:SolidityParser.UncheckedBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#statement.
    def visitStatement(self, ctx:SolidityParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#simpleStatement.
    def visitSimpleStatement(self, ctx:SolidityParser.SimpleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#ifStatement.
    def visitIfStatement(self, ctx:SolidityParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#forStatement.
    def visitForStatement(self, ctx:SolidityParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#whileStatement.
    def visitWhileStatement(self, ctx:SolidityParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:SolidityParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#continueStatement.
    def visitContinueStatement(self, ctx:SolidityParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#breakStatement.
    def visitBreakStatement(self, ctx:SolidityParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#tryStatement.
    def visitTryStatement(self, ctx:SolidityParser.TryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#catchClause.
    def visitCatchClause(self, ctx:SolidityParser.CatchClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#returnStatement.
    def visitReturnStatement(self, ctx:SolidityParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#emitStatement.
    def visitEmitStatement(self, ctx:SolidityParser.EmitStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#revertStatement.
    def visitRevertStatement(self, ctx:SolidityParser.RevertStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#assemblyStatement.
    def visitAssemblyStatement(self, ctx:SolidityParser.AssemblyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#assemblyFlags.
    def visitAssemblyFlags(self, ctx:SolidityParser.AssemblyFlagsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#variableDeclarationList.
    def visitVariableDeclarationList(self, ctx:SolidityParser.VariableDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#variableDeclarationTuple.
    def visitVariableDeclarationTuple(self, ctx:SolidityParser.VariableDeclarationTupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#variableDeclarationStatement.
    def visitVariableDeclarationStatement(self, ctx:SolidityParser.VariableDeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#expressionStatement.
    def visitExpressionStatement(self, ctx:SolidityParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#mappingType.
    def visitMappingType(self, ctx:SolidityParser.MappingTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#mappingKeyType.
    def visitMappingKeyType(self, ctx:SolidityParser.MappingKeyTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulStatement.
    def visitYulStatement(self, ctx:SolidityParser.YulStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulBlock.
    def visitYulBlock(self, ctx:SolidityParser.YulBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulVariableDeclaration.
    def visitYulVariableDeclaration(self, ctx:SolidityParser.YulVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulAssignment.
    def visitYulAssignment(self, ctx:SolidityParser.YulAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulIfStatement.
    def visitYulIfStatement(self, ctx:SolidityParser.YulIfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulForStatement.
    def visitYulForStatement(self, ctx:SolidityParser.YulForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulSwitchCase.
    def visitYulSwitchCase(self, ctx:SolidityParser.YulSwitchCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulSwitchStatement.
    def visitYulSwitchStatement(self, ctx:SolidityParser.YulSwitchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulFunctionDefinition.
    def visitYulFunctionDefinition(self, ctx:SolidityParser.YulFunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulPath.
    def visitYulPath(self, ctx:SolidityParser.YulPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulFunctionCall.
    def visitYulFunctionCall(self, ctx:SolidityParser.YulFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulBoolean.
    def visitYulBoolean(self, ctx:SolidityParser.YulBooleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulLiteral.
    def visitYulLiteral(self, ctx:SolidityParser.YulLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#yulExpression.
    def visitYulExpression(self, ctx:SolidityParser.YulExpressionContext):
        return self.visitChildren(ctx)



del SolidityParser