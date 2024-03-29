from solidity_lexer.SolidityParser import SolidityParser
from solidity_lexer.SolidityParserVisitor import SolidityParserVisitor
from antlr4.error.ErrorListener import ErrorListener

DFG_TYPES = set([
    SolidityParser.SimpleStatementContext,
    SolidityParser.IfStatementContext,
    SolidityParser.ForStatementContext,
    SolidityParser.WhileStatementContext,
    SolidityParser.DoWhileStatementContext,
    SolidityParser.ReturnStatementContext,
    SolidityParser.BlockContext,
    SolidityParser.TryStatementContext]
)

class ParserException(Exception):
    ...

class CustomErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParserException('syntax error, error at line ' + str(line) + ' column ' + str(column) + ' : ' + msg)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        ...

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        ...

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        ...

class CustomVisitor(SolidityParserVisitor):
    def visit(self, tree):
        if tree is None:
            return None
        elif isinstance(tree, list):
            return self.visitChildren(tree)
        else:
            return super().visit(tree)

    def visitChildren(self, nodes):
        results = []
        result = self.defaultResult()
        for node in nodes:
            c_result = node.accept(self)
            result = self.aggregateResult(result, c_result)
            if result is not None:
                results.append(result)
        if len(results) == 0:
            return None
        elif isinstance(results, list) and len(results) == 1:
            return results[0]
        return results
    
    def visitNamedArgument(self, ctx:SolidityParser.NamedArgumentContext):
        res = self.visit(ctx.children)
        return f"{res[0]}:{res[1]}"
    
    def visitCallArgumentList(self, ctx:SolidityParser.CallArgumentListContext):
        res = self.visit(ctx.children)
        if isinstance(res, list):
            return ', '.join(res)
        return res

    def visitIdentifierPath(self, ctx:SolidityParser.IdentifierPathContext):
        return self.visit(ctx.children)
    
    def visitModifierInvocation(self, ctx:SolidityParser.ModifierInvocationContext):
        return self.visit(ctx.children)

    def visitVisibility(self, ctx:SolidityParser.VisibilityContext):
        return self.visit(ctx.children)

    def visitParameterList(self, ctx:SolidityParser.ParameterListContext):
        res =  self.visit(ctx.children)

        if isinstance(res, list):
            return ','.join(res)
        return res
    
    def visitParameterDeclaration(self, ctx:SolidityParser.ParameterDeclarationContext):
        res =  self.visit(ctx.children)
        if len(res) == 2:
            return res[1]
        return None

    def visitConstructorDefinition(self, ctx:SolidityParser.ConstructorDefinitionContext):
        return self.visit(ctx.children)

    def visitStateMutability(self, ctx:SolidityParser.StateMutabilityContext):
        return self.visit(ctx.children)

    def visitOverrideSpecifier(self, ctx:SolidityParser.OverrideSpecifierContext):
        return self.visit(ctx.children)

    def visitFunctionDefinition(self, ctx:SolidityParser.FunctionDefinitionContext):
        res =  self.visit(ctx.children)

        fstr = f'function {res[0]}'
        if ctx.arguments is not None:
            fstr += f"({res[1]})"
        fstr += res[-1]

        return fstr


    def visitModifierDefinition(self, ctx:SolidityParser.ModifierDefinitionContext):
        return self.visit(ctx.children)

    def visitFallbackFunctionDefinition(self, ctx:SolidityParser.FallbackFunctionDefinitionContext):
        return self.visit(ctx.children)

    def visitReceiveFunctionDefinition(self, ctx:SolidityParser.ReceiveFunctionDefinitionContext):
        return self.visit(ctx.children)

    def visitStructDefinition(self, ctx:SolidityParser.StructDefinitionContext):
        return self.visit(ctx.children)

    def visitStructMember(self, ctx:SolidityParser.StructMemberContext):
        return self.visit(ctx.children)

    def visitEnumDefinition(self, ctx:SolidityParser.EnumDefinitionContext):
        return self.visit(ctx.children)

    def visitUserDefinedValueTypeDefinition(self, ctx:SolidityParser.UserDefinedValueTypeDefinitionContext):
        return self.visit(ctx.children)

    def visitStateVariableDeclaration(self, ctx:SolidityParser.StateVariableDeclarationContext):
        return self.visit(ctx.children)

    def visitConstantVariableDeclaration(self, ctx:SolidityParser.ConstantVariableDeclarationContext):
        return self.visit(ctx.children)

    def visitEventParameter(self, ctx:SolidityParser.EventParameterContext):
        return self.visit(ctx.children)

    def visitEventDefinition(self, ctx:SolidityParser.EventDefinitionContext):
        return self.visit(ctx.children)

    def visitErrorParameter(self, ctx:SolidityParser.ErrorParameterContext):
        return self.visit(ctx.children)

    def visitErrorDefinition(self, ctx:SolidityParser.ErrorDefinitionContext):
        return self.visit(ctx.children)

    def visitUserDefinableOperator(self, ctx:SolidityParser.UserDefinableOperatorContext):
        return self.visit(ctx.children)

    def visitUsingDirective(self, ctx:SolidityParser.UsingDirectiveContext):
        return self.visit(ctx.children)

    def visitUsingAliases(self, ctx:SolidityParser.UsingAliasesContext):
        return self.visit(ctx.children)

    def visitTypeName(self, ctx:SolidityParser.TypeNameContext):
        return self.visit(ctx.children)

    def visitElementaryTypeName(self, ctx:SolidityParser.ElementaryTypeNameContext):
        return ctx.getText()

    def visitFunctionTypeName(self, ctx:SolidityParser.FunctionTypeNameContext):
        return self.visit(ctx.children)

    def visitVariableDeclaration(self, ctx:SolidityParser.VariableDeclarationContext):
        res =  self.visit(ctx.children)
        return res[1]

    def visitDataLocation(self, ctx:SolidityParser.DataLocationContext):
        return self.visit(ctx.children)

    def visitUnaryPrefixOperation(self, ctx:SolidityParser.UnaryPrefixOperationContext):
        res = self.visit(ctx.children)
        return f"{ctx.children[0].getText()}{res}"

    def visitPrimaryExpression(self, ctx:SolidityParser.PrimaryExpressionContext):
        return self.visit(ctx.children)

    def visitOrderComparison(self, ctx:SolidityParser.OrderComparisonContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"


    def visitConditional(self, ctx:SolidityParser.ConditionalContext):
        return self.visit(ctx.children)

    def visitPayableConversion(self, ctx:SolidityParser.PayableConversionContext):
        return self.visit(ctx.children)

    def visitAssignment(self, ctx:SolidityParser.AssignmentContext):
        res = self.visit(ctx.children)
        return f'{res[0]}{ctx.children[1].getText()}{res[2]}'

    def visitUnarySuffixOperation(self, ctx:SolidityParser.UnarySuffixOperationContext):
        res = self.visit(ctx.children)
        return f"{res}{ctx.children[1].getText()}"

    def visitShiftOperation(self, ctx:SolidityParser.ShiftOperationContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"

    def visitBitAndOperation(self, ctx:SolidityParser.BitAndOperationContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"

    def visitFunctionCall(self, ctx:SolidityParser.FunctionCallContext):
        res =  self.visit(ctx.children)

        if res[0] in {'require', 'assert', 'revert'}:
            return 
        
        if isinstance(res, list):
            return f"{res[0]}({res[1]})"
        return f"{res}()"

    def visitIndexRangeAccess(self, ctx:SolidityParser.IndexRangeAccessContext):
        res =  self.visit(ctx.children)
        return f"{res[0]}[{res[1]}:{res[2]}]"

    def visitIndexAccess(self, ctx:SolidityParser.IndexAccessContext):
        res = self.visit(ctx.children)
        return f"{res[0]}[{res[1]}]"

    def visitAddSubOperation(self, ctx:SolidityParser.AddSubOperationContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"

    def visitBitOrOperation(self, ctx:SolidityParser.BitOrOperationContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"

    def visitExpOperation(self, ctx:SolidityParser.ExpOperationContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"
    
    def visitAndOperation(self, ctx:SolidityParser.AndOperationContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"
    
    def visitInlineArray(self, ctx:SolidityParser.InlineArrayContext):
        return self.visit(ctx.children)

    def visitOrOperation(self, ctx:SolidityParser.OrOperationContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"

    def visitMemberAccess(self, ctx:SolidityParser.MemberAccessContext):
        res =  self.visit(ctx.children)
        return f"{res[0]}.{res[1]}"

    def visitMulDivModOperation(self, ctx:SolidityParser.MulDivModOperationContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"

    def visitFunctionCallOptions(self, ctx:SolidityParser.FunctionCallOptionsContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{{{res[1]}}}"

    def visitNewExpr(self, ctx:SolidityParser.NewExprContext):
        return self.visit(ctx.children)

    def visitBitXorOperation(self, ctx:SolidityParser.BitXorOperationContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"

    def visitTuple(self, ctx:SolidityParser.TupleContext):
        res = self.visit(ctx.children)
        if isinstance(res, list):
            return f"({','.join(res)})"
        return f"({res},)"
    
    def visitEqualityComparison(self, ctx:SolidityParser.EqualityComparisonContext):
        res = self.visit(ctx.children)
        return f"{res[0]}{ctx.children[1].getText()}{res[1]}"
    
    def visitMetaType(self, ctx:SolidityParser.MetaTypeContext):
        return self.visit(ctx.children)

    def visitAssignOp(self, ctx:SolidityParser.AssignOpContext):
        return ctx.getText()

    def visitTupleExpression(self, ctx:SolidityParser.TupleExpressionContext):
        return self.visit(ctx.children)

    def visitInlineArrayExpression(self, ctx:SolidityParser.InlineArrayExpressionContext):
        return self.visit(ctx.children)
    
    def visitIdentifier(self, ctx:SolidityParser.IdentifierContext):
        return ctx.getText()

    def visitLiteral(self, ctx:SolidityParser.LiteralContext):
        return ctx.getText()
    
    def visitLiteralWithSubDenomination(self, ctx:SolidityParser.LiteralWithSubDenominationContext):
        base = ctx.children[0].getText()
        sub = ctx.children[1].getText()

        return f"{base}{sub}"
    
    def visitBlock(self, ctx:SolidityParser.BlockContext):
        res =  self.visit(ctx.children)

        if isinstance(res, list):
            return f"{{{';'.join(res)}}}"
        if res is not None:
            return f"{{{res}}}"
        return "{}"

    def visitUncheckedBlock(self, ctx:SolidityParser.UncheckedBlockContext):
        res = self.visit(ctx.children)
        if isinstance(res, list):
            return f"{{{';'.join(res)}}}"
        if res is not None:
            return f"{{{res}}}"
        return "{}"

    def visitStatement(self, ctx:SolidityParser.StatementContext):
        if type(ctx.children[0]) in DFG_TYPES:
            return self.visit(ctx.children)
        else: self.visit(ctx.children)

    def visitSimpleStatement(self, ctx:SolidityParser.SimpleStatementContext):
        return self.visit(ctx.children)

    def visitIfStatement(self, ctx:SolidityParser.IfStatementContext):
        print(ctx.getText())
        res =  self.visit(ctx.children)
        cond = res[0]
        if len(res) == 2:
            return f"({cond}?{res[1]})"
        else:
            return f"({cond}?{res[1]}:{res[2]})"

    def visitForStatement(self, ctx:SolidityParser.ForStatementContext):
        res =  self.visit(ctx.children)
        start = cond = end = ''

        if isinstance(res, str):
            return f"(()=>{res})"

        if isinstance(ctx.children[2], SolidityParser.SimpleStatementContext):
            start = res[0] + ';' if res[0] else ''

            if isinstance(ctx.children[3], SolidityParser.ExpressionStatementContext):
                cond = res[1]
            if len(res) == 4:
                end = res[2] + ';' if res[2] else ''
            
        elif isinstance(ctx.children[3], SolidityParser.ExpressionStatementContext):
            cond = res[0]

            if len(res) == 3:
                end = res[1] + ';' if res[1] else ''
        elif len(res) == 2:
            end = res[1] + ';' if res[1] else ''

        body = res[-1]

        fstr = f"{start}(({cond})=>{body}{end})"
        return fstr

    def visitWhileStatement(self, ctx:SolidityParser.WhileStatementContext):
        res = self.visit(ctx.children)
        cond = res[0]
        body = res[1]
        return f"({cond}=>{body})"

    def visitDoWhileStatement(self, ctx:SolidityParser.DoWhileStatementContext):
        res = self.visit(ctx.children)
        cond = res[1]
        body = res[0]
        return f"{body}({cond}=>{body})"

    def visitContinueStatement(self, ctx:SolidityParser.ContinueStatementContext):
        return self.visit(ctx.children)

    def visitBreakStatement(self, ctx:SolidityParser.BreakStatementContext):
        return self.visit(ctx.children)

    def visitTryStatement(self, ctx:SolidityParser.TryStatementContext):
        res =  self.visit(ctx.children)
        ext_func = res[0]
        body = res[1]
        catch_body = res[2]
        return f"({ext_func}?{body}:{catch_body})"

    def visitCatchClause(self, ctx:SolidityParser.CatchClauseContext):
        res =  self.visit(ctx.children)
        return res[-1]

    def visitReturnStatement(self, ctx:SolidityParser.ReturnStatementContext):
        return f"return{{{self.visit(ctx.children)}}}"

    def visitEmitStatement(self, ctx:SolidityParser.EmitStatementContext):
        return self.visit(ctx.children)

    def visitRevertStatement(self, ctx:SolidityParser.RevertStatementContext):
        return self.visit(ctx.children)

    def visitAssemblyStatement(self, ctx:SolidityParser.AssemblyStatementContext):
        return self.visit(ctx.children)

    def visitAssemblyFlags(self, ctx:SolidityParser.AssemblyFlagsContext):
        return self.visit(ctx.children)

    def visitVariableDeclarationList(self, ctx:SolidityParser.VariableDeclarationListContext):
        return self.visit(ctx.children)

    def visitVariableDeclarationTuple(self, ctx:SolidityParser.VariableDeclarationTupleContext):
        res = self.visit(ctx.children)
        if isinstance(res, list):
            return f"({','.join(res)})"
        return f"({res},)"

    def visitVariableDeclarationStatement(self, ctx:SolidityParser.VariableDeclarationStatementContext):
        res =  self.visit(ctx.children)
        if len(res) == 1:
            return res[0]
        return f"{res[0]}={res[1]}"

    def visitExpressionStatement(self, ctx:SolidityParser.ExpressionStatementContext):
        return self.visit(ctx.children)

    def visitMappingType(self, ctx:SolidityParser.MappingTypeContext):
        return self.visit(ctx.children)

    def visitMappingKeyType(self, ctx:SolidityParser.MappingKeyTypeContext):
        return self.visit(ctx.children)

    def visitYulStatement(self, ctx:SolidityParser.YulStatementContext):
        return self.visit(ctx.children)

    def visitYulBlock(self, ctx:SolidityParser.YulBlockContext):
        return self.visit(ctx.children)

    def visitYulVariableDeclaration(self, ctx:SolidityParser.YulVariableDeclarationContext):
        return self.visit(ctx.children)

    def visitYulAssignment(self, ctx:SolidityParser.YulAssignmentContext):
        return self.visit(ctx.children)

    def visitYulIfStatement(self, ctx:SolidityParser.YulIfStatementContext):
        return self.visit(ctx.children)

    def visitYulForStatement(self, ctx:SolidityParser.YulForStatementContext):
        return self.visit(ctx.children)

    def visitYulSwitchCase(self, ctx:SolidityParser.YulSwitchCaseContext):
        return self.visit(ctx.children)

    def visitYulSwitchStatement(self, ctx:SolidityParser.YulSwitchStatementContext):
        return self.visit(ctx.children)

    def visitYulFunctionDefinition(self, ctx:SolidityParser.YulFunctionDefinitionContext):
        return self.visit(ctx.children)

    def visitYulPath(self, ctx:SolidityParser.YulPathContext):
        return self.visit(ctx.children)

    def visitYulFunctionCall(self, ctx:SolidityParser.YulFunctionCallContext):
        return self.visit(ctx.children)

    def visitYulBoolean(self, ctx:SolidityParser.YulBooleanContext):
        return self.visit(ctx.children)
 
    def visitYulLiteral(self, ctx:SolidityParser.YulLiteralContext):
        return self.visit(ctx.children)

    def visitYulExpression(self, ctx:SolidityParser.YulExpressionContext):
        return self.visit(ctx.children)
    
    